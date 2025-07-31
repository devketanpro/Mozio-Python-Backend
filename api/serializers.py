from django.contrib.gis.geos import GEOSGeometry
from rest_framework import serializers

from .models import Provider, ServiceArea


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"


class ServiceAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = "__all__"

    def validate_area(self, value):
        if isinstance(value, dict):
            try:
                return GEOSGeometry(
                    str(value).replace("'", '"')
                )  # Ensure JSON string format
            except Exception as e:
                raise serializers.ValidationError(f"Invalid polygon geometry: {e}")
        return value
