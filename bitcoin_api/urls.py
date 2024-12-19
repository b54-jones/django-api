from django.urls import path, include
from .views import BitcoinInfoView

urlpatterns = [
    path('', BitcoinInfoView.as_view(), name='bitcoin-info'),
]