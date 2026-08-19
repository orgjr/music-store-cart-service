from uuid import uuid4

from django.urls import reverse
from rest_framework import status

from services.cart_service import CartService
from tests.cart.test_endpoints.base import CART_LIST_URL, CartEndpointApiTestCase


class CartListEndpointTests(CartEndpointApiTestCase):
    def test_cart_list_url_name(self):
        self.assertEqual(reverse("cart-list"), CART_LIST_URL)

    def test_cart_list_is_paginated(self):
        CartService.get_or_create_cart(uuid4())
        response = self.client.get(CART_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("count", body)
        self.assertIn("next", body)
        self.assertIn("previous", body)
        self.assertIn("results", body)
        self.assertEqual(body["count"], 2)

    def test_cart_list_rejects_patch(self):
        response = self.client.patch(CART_LIST_URL, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
