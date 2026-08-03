from django.urls import reverse
from rest_framework import status

from tests.cart.test_endpoints.base import CartItemApiTestCase


class CartItemDetailEndpointTests(CartItemApiTestCase):
    def test_item_detail_url_name(self):
        item = self.create_item()
        self.assertEqual(
            reverse("cart-item-detail", args=[item.pk]),
            f"/api/v1/cart/items/{item.pk}/",
        )

    def test_retrieve_item(self):
        item = self.create_item()
        response = self.client.get(f"/api/v1/cart/items/{item.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["product_id"], 10)

    def test_retrieve_missing_item_returns_404(self):
        response = self.client.get("/api/v1/cart/items/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)