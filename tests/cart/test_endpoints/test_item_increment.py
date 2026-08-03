from django.urls import reverse
from rest_framework import status

from tests.cart.test_endpoints.base import CartItemApiTestCase


class CartItemIncrementEndpointTests(CartItemApiTestCase):
    def item_url(self, item):
        return f"/api/v1/cart/items/{item.pk}/increment/"

    def test_item_increment_url_name(self):
        item = self.create_item()
        self.assertEqual(
            reverse("cart-item-increment", args=[item.pk]),
            f"/api/v1/cart/items/{item.pk}/increment/",
        )

    def test_increment_item(self):
        item = self.create_item(quantity=1)
        response = self.client.post(self.item_url(item))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["quantity"], 2)
        self.assert_cart_price("2500.00")

    def test_increment_rejects_get(self):
        item = self.create_item()
        response = self.client.get(
            reverse("cart-item-increment", args=[item.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)