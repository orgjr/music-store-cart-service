from rest_framework import status

from cart.models import CartItem
from tests.cart.test_endpoints.base import CartItemApiTestCase


class CartItemUpdateEndpointTests(CartItemApiTestCase):
    def item_url(self, item):
        return f"/api/v1/cart/items/{item.pk}/"

    def test_partial_update_sets_quantity(self):
        item = self.create_item(quantity=2)
        response = self.client.patch(
            self.item_url(item), {"quantity": 3}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["quantity"], 3)
        self.assert_cart_price("3750.00")

    def test_partial_update_quantity_zero_removes_item(self):
        item = self.create_item(quantity=5)
        response = self.client.patch(
            self.item_url(item), {"quantity": 0}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(pk=item.pk).exists())
        self.assert_cart_price("0.00")

    def test_partial_update_negative_quantity_returns_500(self):
        item = self.create_item(quantity=5)
        self.client.raise_request_exception = False
        response = self.client.patch(
            self.item_url(item),
            {"quantity": -2},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_full_put_sets_quantity(self):
        item = self.create_item(quantity=2)
        payload = self.item_payload(quantity=1)
        self.client.raise_request_exception = False
        response = self.client.put(self.item_url(item), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
