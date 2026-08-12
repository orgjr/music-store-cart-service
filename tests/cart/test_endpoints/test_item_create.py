from rest_framework import status

from cart.models import CartItem
from tests.cart.test_endpoints.base import (
    CART_ITEM_LIST_URL,
    CartItemApiTestCase,
)


class CartItemCreateEndpointTests(CartItemApiTestCase):
    def test_add_item_creates_item(self):
        response = self.add_item(quantity=2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertEqual(body["product_id"], 10)
        self.assertEqual(body["quantity"], 2)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_add_duplicate_item_sums_quantity(self):
        self.add_item(quantity=2)
        response = self.add_item(quantity=3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["quantity"], 5)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_add_item_recalculates_cart_price(self):
        self.add_item(product_id=1, price="1000.00", quantity=2)
        self.add_item(product_id=2, price="250.00", quantity=2)
        self.assert_cart_price("2500.00")

    def test_add_item_requires_required_fields(self):
        payload = self.item_payload()
        del payload["product_name"]
        response = self.client.post(CART_ITEM_LIST_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("product_name", response.json())

    def test_add_item_with_invalid_cart_returns_400(self):
        payload = self.item_payload()
        payload["cart"] = "00000000-0000-0000-0000-000000000000"
        response = self.client.post(CART_ITEM_LIST_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("cart", response.json())

    def test_add_item_quantity_zero_returns_400(self):
        response = self.client.post(
            CART_ITEM_LIST_URL,
            self.item_payload(quantity=0),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_add_item_with_negative_quantity_returns_400(self):
        response = self.add_item(quantity=-1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("quantity", response.json())
        self.assertEqual(CartItem.objects.count(), 0)

    def test_add_item_with_negative_product_id_returns_400(self):
        payload = self.item_payload(product_id=-1)
        response = self.client.post(CART_ITEM_LIST_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("product_id", response.json())
        self.assertEqual(CartItem.objects.count(), 0)
