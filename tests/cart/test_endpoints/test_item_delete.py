from rest_framework import status

from cart.models import CartItem
from tests.cart.test_endpoints.base import CartItemApiTestCase


class CartItemDeleteEndpointTests(CartItemApiTestCase):
    def test_delete_item(self):
        item = self.create_item()
        response = self.client.delete(f"/api/v1/cart/items/{item.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(pk=item.pk).exists())
        self.assert_cart_price("0.00")

    def test_delete_missing_item_returns_404(self):
        response = self.client.delete("/api/v1/cart/items/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)