from rest_framework import serializers
from .models import URLInfo

class URLInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLInfo
        fields = ['id', 'url', 'domain_name', 'protocol', 'title', 'image', 'stylesheets']