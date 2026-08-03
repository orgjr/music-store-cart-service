from rest_framework import status
from rest_framework.test import APITestCase

from tests.cart.test_endpoints.base import CART_LIST_URL


class CartCreateEndpointTests(APITestCase):
    def test_create_cart_returns_empty_cart_shape(self):
        response = self.client.post(CART_LIST_URL, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertEqual(body["price"], "0.00")
        self.assertEqual(body["items"], [])