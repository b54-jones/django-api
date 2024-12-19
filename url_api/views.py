from django.shortcuts import render
from bs4 import BeautifulSoup
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from urllib.parse import urlparse
from .models import URLInfo
from .serializers import URLInfoSerializer
import requests

# Create your views here.
class URLAnalysisView(viewsets.ModelViewSet):
    queryset = URLInfo.objects.all()
    serializer_class = URLInfoSerializer

    def try_to_get_url(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Request failed: {str(e)}")

    def get_data_from_url(self, url):
        parsed_url = urlparse(url)
        protocol = parsed_url.scheme
        if not protocol:
            raise ValueError("URL does not have a protocol so it is invalid")
        domain_name = parsed_url.netloc
        return protocol, domain_name

    def get_data_from_page(self, page):
        soup = BeautifulSoup(page, 'html.parser')

        image_links = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]
        num_stylesheets = len(soup.find_all('link', {'rel': 'stylesheet'}) + soup.find_all('style'))
        title = soup.title.string.strip() if soup.title and soup.title.string else None

        return image_links, num_stylesheets, title

    def save_url_info(self, url, image_links, num_stylesheets, title, protocol, domain_name):
        url_info, created = URLInfo.objects.get_or_create(
            url=url,
            defaults={
                'image': image_links,
                'domain_name': domain_name,
                'stylesheets': num_stylesheets,
                'title': title,
                'protocol': protocol
            }
        )

        if not created:
            url_info.image = image_links
            url_info.domain_name = domain_name
            url_info.stylesheets = num_stylesheets
            url_info.title = title
            url_info.protocol = protocol
            url_info.save()

        return url_info, created

    def create(self, request, *args, **kwargs):
        url = request.data.get('url')
        if not url:
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

        response = self.try_to_get_url(url)

        protocol, domain_name = self.get_data_from_url(url)

        image_links, num_stylesheets,title = self.get_data_from_page(response.content)

        url_info, created = self.save_url_info(url, image_links, num_stylesheets, title, protocol, domain_name)

        serializer = URLInfoSerializer(url_info)

        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

