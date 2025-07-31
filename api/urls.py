from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AuthViewSet, ProviderViewSet, ServiceAreaViewSet, service_area_lookup

router = DefaultRouter()
router.register(r"providers", ProviderViewSet)
router.register(r"service-areas", ServiceAreaViewSet)
router.register(r"auth", AuthViewSet, basename="auth")

urlpatterns = router.urls + [
    path("lookup-service-area/", service_area_lookup),
]
