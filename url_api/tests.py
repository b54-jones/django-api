import pytest
import requests
from unittest.mock import patch
from .views import URLAnalysisView

@pytest.fixture
def url_analysis_view():
    return URLAnalysisView()

@patch('requests.get')
def test_try_to_get_url_success(mock_get, url_analysis_view):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.text = 'content'
    url = 'https://validurl.com'

    response = url_analysis_view.try_to_get_url(url)

    mock_get.assert_called_once_with(url, timeout=10)
    assert response.status_code == 200

@patch('requests.get')
def test_try_to_get_url_fail(mock_get, url_analysis_view):
    mock_get.side_effect = requests.exceptions.RequestException('Request failed')
    url = 'https://invalidurl.com'

    with pytest.raises(ValueError):
        url_analysis_view.try_to_get_url(url)

def test_get_data_from_url(url_analysis_view):
    protocol, domain_name = url_analysis_view.get_data_from_url("https://example.com")

    assert protocol == 'https'
    assert domain_name == 'example.com'

def test_get_data_from_url_no_protocol(url_analysis_view):
    with pytest.raises(ValueError):
        protocol, domain_name = url_analysis_view.get_data_from_url("example.com")

def test_get_data_from_page(url_analysis_view):
    html_content = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <img src="image1.jpg">
            <img src="image2.jpg">
            <link rel="stylesheet" href="style.css">
            <style>body { background-color: blue; }</style>
        </body>
    </html>
    """

    image_links, num_stylesheets, title = url_analysis_view.get_data_from_page(html_content)

    assert len(image_links) == 2
    assert image_links == ['image1.jpg', 'image2.jpg']
    assert num_stylesheets == 2
    assert title == 'Test Page'