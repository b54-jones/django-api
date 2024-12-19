from django.urls import path, include
from .views import URLAnalysisView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', URLAnalysisView)

urlpatterns = [
    path('', include(router.urls)),
]