from django.test import SimpleTestCase
from rest_framework import status

API_ROOT = "/api/v1"


class DocsUISmokeTests(SimpleTestCase):
    def test_swagger_ui_endpoint_responds(self):
        response = self.client.get(API_ROOT + "/docs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_redoc_ui_endpoint_responds(self):
        response = self.client.get(API_ROOT + "/redoc/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)