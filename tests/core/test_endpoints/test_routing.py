from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework import status

API_ROOT = "/api/v1"


class RoutingSmokeTests(SimpleTestCase):
    def test_unknown_route_returns_404(self):
        response = self.client.get(API_ROOT + "/does-not-exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_url_names_resolve(self):
        self.assertEqual(reverse("index"), API_ROOT + "/")
        self.assertEqual(reverse("health"), API_ROOT + "/health/")
        self.assertEqual(reverse("schema"), API_ROOT + "/schema/")
        self.assertEqual(reverse("swagger-ui"), API_ROOT + "/docs/")
        self.assertEqual(reverse("redoc"), API_ROOT + "/redoc/")