from uuid import uuid4

from rest_framework import status
from rest_framework.test import APITestCase

from cart.models import Cart
from tests.core.test_functional.base import ITEM_PAYLOAD

API_ROOT = "/api/v1"


class ErrorHandlingFunctionalTests(APITestCase):
    def item_payload(self):
        cart = Cart.objects.create()
        return dict(ITEM_PAYLOAD, cart=str(cart.pk))

    def test_unknown_cart_detail_returns_404(self):
        response = self.client.get(f"{API_ROOT}/cart/{uuid4()}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_missing_cart_clear_returns_404(self):
        response = self.client.delete(f"{API_ROOT}/cart/{uuid4()}/items/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_item_payload_returns_400(self):
        payload = self.item_payload()
        payload["quantity"] = -1
        response = self.client.post(f"{API_ROOT}/cart/items/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_cart_method_returns_405(self):
        response = self.client.patch(f"{API_ROOT}/cart/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
