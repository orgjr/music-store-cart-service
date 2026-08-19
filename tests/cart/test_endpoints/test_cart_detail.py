from django.urls import reverse
from rest_framework import status

from tests.cart.test_endpoints.base import CartEndpointApiTestCase


class CartDetailEndpointTests(CartEndpointApiTestCase):
    def test_cart_detail_url_name(self):
        self.assertEqual(
            reverse("cart-detail", args=[self.cart.pk]),
            f"/api/v1/cart/{self.cart.pk}/",
        )

    def test_cart_detail_with_invalid_uuid_returns_404(self):
        response = self.client.get("/api/v1/cart/not-a-uuid/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
