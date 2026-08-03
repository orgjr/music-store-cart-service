from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from cart.models import CartItem
from cart.services.cart_service import CartService

CART_LIST_URL = "/api/v1/cart/"
CART_ITEM_LIST_URL = "/api/v1/cart/items/"


class CartApiMixin:
    def item_payload(
        self, product_id=10, name="Fender Stratocaster", price="1250.00", quantity=1
    ):
        return {
            "cart": str(self.cart.pk),
            "product_id": product_id,
            "product_name": name,
            "product_slug": name.replace(" ", "-").lower(),
            "unit_price": price,
            "image_url": f"https://cdn.example.com/img/{product_id}.jpg",
            "quantity": quantity,
        }

    def add_item(self, **overrides):
        return self.client.post(
            CART_ITEM_LIST_URL, self.item_payload(**overrides), format="json"
        )

    def get_cart(self, uuid=None):
        return self.client.get(f"/api/v1/cart/{uuid or self.cart.pk}/")

    def assert_cart_price(self, expected):
        response = self.get_cart()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["price"], str(expected))

    def create_item(self, product_id=10, quantity=1, **overrides):
        defaults = {
            "product_name": "Fender Stratocaster",
            "product_slug": "fender-stratocaster",
            "unit_price": Decimal("1250.00"),
            "image_url": "https://cdn.example.com/img/10.jpg",
            "quantity": quantity,
        }
        defaults.update(overrides)
        return CartItem.objects.create(
            cart=self.cart, product_id=product_id, **defaults
        )


class CartEndpointApiTestCase(CartApiMixin, APITestCase):
    def setUp(self):
        self.cart, _ = CartService.get_or_create_cart()
        self.item = self.create_item()


class CartItemApiTestCase(CartApiMixin, APITestCase):
    def setUp(self):
        self.cart, _ = CartService.get_or_create_cart()