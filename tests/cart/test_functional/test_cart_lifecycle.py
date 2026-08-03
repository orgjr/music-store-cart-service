from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from cart.models import Cart, CartItem
from tests.cart.test_endpoints.base import (
    CART_LIST_URL,
    CartApiMixin,
)


class CartLifecycleFunctionalTests(CartApiMixin, APITestCase):
    def setUp(self):
        response = self.client.post(CART_LIST_URL, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.cart_uuid = response.json()["uuid"]
        self.cart = Cart.objects.get(pk=self.cart_uuid)

    def test_full_cart_lifecycle_through_the_api(self):
        response = self.add_item(quantity=2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assert_cart_price(Decimal("2500.00"))

        response = self.add_item(quantity=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_cart_price(Decimal("3750.00"))
        item_id = response.json()["id"]
        self.assertEqual(response.json()["quantity"], 3)

        url = f"/api/v1/cart/items/{item_id}/"
        response = self.client.patch(url, {"quantity": 2}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["quantity"], 5)
        self.assert_cart_price(Decimal("6250.00"))

        response = self.client.post(f"{url}increment/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["quantity"], 6)

        response = self.client.post(f"{url}decrement/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["quantity"], 5)
        self.assert_cart_price(Decimal("6250.00"))

        response = self.client.delete(f"/api/v1/cart/{self.cart_uuid}/items/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.price, Decimal("0.00"))
        self.assertEqual(self.cart.items.count(), 0)

        response = self.client.delete(f"/api/v1/cart/{self.cart_uuid}/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Cart.objects.filter(pk=self.cart_uuid).exists())

    def test_cart_can_be_reused_after_being_cleared(self):
        self.add_item(quantity=1)
        self.client.delete(f"/api/v1/cart/{self.cart_uuid}/items/")
        response = self.add_item(product_id=20, name="Yamaha U1 Piano", price="4500.00")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assert_cart_price(Decimal("4500.00"))
        self.assertEqual(CartItem.objects.filter(cart=self.cart).count(), 1)