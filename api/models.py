from django.contrib.gis.db import models as geomodels
from django.db import models

from accounts.models import User


class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name="service_areas"
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    area = geomodels.PolygonField()

    def __str__(self):
        return self.name
