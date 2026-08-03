import json

from django.conf import settings
from django.test import SimpleTestCase
from rest_framework import status

API_ROOT = "/api/v1"


class OpenAPISchemaEndpointSmokeTests(SimpleTestCase):
    def test_openapi_schema_endpoint_responds(self):
        response = self.client.get(
            API_ROOT + "/schema/",
            HTTP_ACCEPT="application/vnd.oai.openapi+json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/vnd.oai.openapi+json")
        schema = json.loads(response.content)
        self.assertEqual(schema["openapi"][:3], "3.0")
        self.assertEqual(schema["info"]["title"], settings.PROJECT_NAME)