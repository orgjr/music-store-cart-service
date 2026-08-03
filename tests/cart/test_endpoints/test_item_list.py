from django.urls import reverse
from rest_framework import status

from tests.cart.test_endpoints.base import (
    CART_ITEM_LIST_URL,
    CartItemApiTestCase,
)


class CartItemListEndpointTests(CartItemApiTestCase):
    def test_cart_item_list_url_name(self):
        self.assertEqual(reverse("cart-item-list"), CART_ITEM_LIST_URL)

    def test_list_items_is_paginated(self):
        self.add_item()
        self.add_item(product_id=20, name="Yamaha U1 Piano")
        response = self.client.get(CART_ITEM_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("results", body)
        self.assertEqual(body["count"], 2)