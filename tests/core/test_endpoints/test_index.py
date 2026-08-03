from django.conf import settings
from django.test import SimpleTestCase
from rest_framework import status

API_ROOT = "/api/v1"


class IndexEndpointSmokeTests(SimpleTestCase):
    def test_index_endpoint_responds(self):
        response = self.client.get(API_ROOT + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["name"], settings.PROJECT_NAME)
        self.assertEqual(body["environment"], settings.ENVIRONMENT)
        self.assertEqual(body["api_version"], "v1")
        self.assertEqual(body["redoc_url"], API_ROOT + "/redoc/")
        self.assertEqual(body["health_url"], API_ROOT + "/health/")