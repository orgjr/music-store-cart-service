from django.urls import reverse

from tests.cart.test_endpoints.base import CartEndpointApiTestCase


class CartClearEndpointTests(CartEndpointApiTestCase):
    def test_cart_clear_url_name(self):
        self.assertEqual(
            reverse("cart-clear", args=[self.cart.pk]),
            f"/api/v1/cart/{self.cart.pk}/items/",
        )