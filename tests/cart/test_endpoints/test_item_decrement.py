from django.urls import reverse
from rest_framework import status

from cart_item.models import CartItem
from tests.cart.test_endpoints.base import CartItemApiTestCase


class CartItemDecrementEndpointTests(CartItemApiTestCase):
    def item_url(self, item):
        return f"/api/v1/cart/items/{item.pk}/decrement/"

    def test_item_decrement_url_name(self):
        item = self.create_item()
        self.assertEqual(
            reverse("cart-item-decrement", args=[item.pk]),
            f"/api/v1/cart/items/{item.pk}/decrement/",
        )

    def test_decrement_item(self):
        item = self.create_item(quantity=3)
        response = self.client.post(self.item_url(item))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["quantity"], 2)
        self.assert_cart_price("2500.00")

    def test_decrement_removes_item_when_quantity_reaches_zero(self):
        item = self.create_item(quantity=1)
        response = self.client.post(self.item_url(item))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(pk=item.pk).exists())
        self.assert_cart_price("0.00")
