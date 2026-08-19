from rest_framework import status

from cart_item.models import CartItem
from tests.cart.test_endpoints.base import CART_ITEM_LIST_URL, CartItemApiTestCase


class CartItemCreateEndpointTests(CartItemApiTestCase):
    def test_add_item_creates_item(self):
        product = self.register_product(
            "fender-stratocaster", name="Fender Stratocaster", price="1250.00"
        )
        response = self.add_item(slug=product["slug"], quantity=2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertEqual(body["product_id"], product["uuid"])
        self.assertEqual(body["product_slug"], product["slug"])
        self.assertEqual(body["quantity"], 2)
        self.assertEqual(body["price"], "2500.00")
        self.assertEqual(CartItem.objects.count(), 1)

    def test_add_duplicate_item_sums_quantity(self):
        product = self.register_product(
            "fender-stratocaster", name="Fender Stratocaster", price="1250.00"
        )
        self.add_item(slug=product["slug"], quantity=2)
        response = self.add_item(slug=product["slug"], quantity=3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["quantity"], 5)
        self.assertEqual(body["price"], "6250.00")
        self.assertEqual(CartItem.objects.count(), 1)

    def test_add_item_recalculates_cart_price(self):
        self.register_product(
            "gibson-les-paul", name="Gibson Les Paul", price="1000.00"
        )
        self.register_product("pearl-export", name="Pearl Export", price="250.00")
        self.add_item(slug="gibson-les-paul", quantity=2)
        self.add_item(slug="pearl-export", quantity=2)
        self.assert_cart_price("2500.00")

    def test_add_item_requires_product_slug(self):
        payload = self.item_payload()
        del payload["product_slug"]
        response = self.client.post(CART_ITEM_LIST_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("product_slug", response.json())

    def test_add_item_requires_quantity(self):
        payload = self.item_payload()
        del payload["quantity"]
        response = self.client.post(CART_ITEM_LIST_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("quantity", response.json())

    def test_add_item_with_invalid_cart_returns_400(self):
        payload = self.item_payload()
        payload["cart"] = "00000000-0000-0000-0000-000000000000"
        response = self.client.post(CART_ITEM_LIST_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("cart", response.json())

    def test_add_item_quantity_zero_returns_400(self):
        response = self.add_item(quantity=0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("quantity", response.json())
        self.assertEqual(CartItem.objects.count(), 0)

    def test_add_item_with_negative_quantity_returns_400(self):
        response = self.add_item(quantity=-1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("quantity", response.json())
        self.assertEqual(CartItem.objects.count(), 0)
