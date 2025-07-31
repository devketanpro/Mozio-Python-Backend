from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Polygon
from rest_framework.test import APIClient, APITestCase

from .models import Provider, ServiceArea


class BaseTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123", email="test@example.com"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.provider = Provider.objects.create(
            user=self.user,
            name="Test Provider",
            email="provider@example.com",
            phone_number="1234567890",
            language="en",
            currency="USD",
        )

        self.polygon = Polygon(
            (
                (0.0, 0.0),
                (0.0, 10.0),
                (10.0, 10.0),
                (10.0, 0.0),
                (0.0, 0.0),
            )
        )

        self.service_area = ServiceArea.objects.create(
            provider=self.provider, name="Test Area", price=100.00, area=self.polygon
        )


class ProviderAPITestCase(BaseTestCase):
    def test_list_providers(self):
        response = self.client.get("/api/providers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_provider(self):
        new_user = get_user_model().objects.create_user(
            username="anotheruser", email="another@example.com", password="pass1234"
        )
        payload = {
            "user": new_user.id,
            "name": "New Provider",
            "email": "new@example.com",
            "phone_number": "9999999999",
            "language": "fr",
            "currency": "EUR",
        }
        response = self.client.post("/api/providers/", payload)
        self.assertEqual(response.status_code, 201)

    def test_retrieve_provider(self):
        response = self.client.get(f"/api/providers/{self.provider.id}/")
        self.assertEqual(response.status_code, 200)

    def test_update_provider(self):
        response = self.client.patch(
            f"/api/providers/{self.provider.id}/", {"language": "es"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["language"], "es")

    def test_delete_provider(self):
        response = self.client.delete(f"/api/providers/{self.provider.id}/")
        self.assertEqual(response.status_code, 204)


class ServiceAreaAPITestCase(BaseTestCase):
    def test_list_service_areas(self):
        response = self.client.get("/api/service-areas/")
        self.assertEqual(response.status_code, 200)

    def test_create_service_area(self):
        payload = {
            "provider": self.provider.id,
            "name": "New Area",
            "price": 250.00,
            "area": {
                "type": "Polygon",
                "coordinates": [
                    [[0.0, 0.0], [0.0, 5.0], [5.0, 5.0], [5.0, 0.0], [0.0, 0.0]]
                ],
            },
        }
        response = self.client.post("/api/service-areas/", payload, format="json")
        self.assertEqual(response.status_code, 201)

    def test_retrieve_service_area(self):
        response = self.client.get(f"/api/service-areas/{self.service_area.id}/")
        self.assertEqual(response.status_code, 200)

    def test_update_service_area(self):
        response = self.client.patch(
            f"/api/service-areas/{self.service_area.id}/", {"price": 999.99}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(float(response.data["price"]), 999.99)

    def test_delete_service_area(self):
        response = self.client.delete(f"/api/service-areas/{self.service_area.id}/")
        self.assertEqual(response.status_code, 204)


class ServiceAreaLookupAPITestCase(BaseTestCase):
    def test_lookup_service_area_inside(self):
        response = self.client.get("/api/lookup-service-area/?lat=5&lng=5")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["service_area"], "Test Area")

    def test_lookup_service_area_outside(self):
        response = self.client.get("/api/lookup-service-area/?lat=20&lng=20")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_lookup_invalid_coords(self):
        response = self.client.get("/api/lookup-service-area/?lat=abc&lng=xyz")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
