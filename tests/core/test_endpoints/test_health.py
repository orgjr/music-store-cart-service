from django.test import SimpleTestCase
from rest_framework import status

API_ROOT = "/api/v1"


class HealthEndpointSmokeTests(SimpleTestCase):
    def test_health_endpoint_responds(self):
        response = self.client.get(API_ROOT + "/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["status"], "ok")
        self.assertIsInstance(body["uptime_seconds"], (int, float))
        self.assertGreaterEqual(body["uptime_seconds"], 0)