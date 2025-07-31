from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from rest_framework import status, viewsets
from rest_framework.decorators import (
    action,
    api_view,
    permission_classes,
    throttle_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import SignupSerializer

from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer

User = get_user_model()


class AuthViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["post"], url_path="signup")
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "email": user.email,
                "username": user.username,
            },
            status=status.HTTP_201_CREATED,
        )


class ProviderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ServiceAreaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def service_area_lookup(request):
    try:
        lat = float(request.query_params.get("lat"))
        lng = float(request.query_params.get("lng"))
        point = Point(lng, lat)
    except (TypeError, ValueError):
        return Response({"error": "Invalid lat/lng"}, status=400)

    areas = ServiceArea.objects.filter(area__contains=point).select_related("provider")
    data = [
        {"service_area": area.name, "price": area.price, "provider": area.provider.name}
        for area in areas
    ]
    return Response(data)
