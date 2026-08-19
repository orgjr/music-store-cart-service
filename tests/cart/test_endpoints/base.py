from decimal import Decimal
from uuid import uuid4

from rest_framework import status
from rest_framework.test import APITestCase

from cart_item.models import CartItem
from services.cart_service import CartService
from tests.base import ProductServiceMockMixin

CART_LIST_URL = "/api/v1/cart/"
CART_ITEM_LIST_URL = "/api/v1/cart/items/"


class CartApiMixin(ProductServiceMockMixin):
    DEFAULT_PRODUCT = "fender-stratocaster"

    def item_payload(self, slug=None, quantity=1):
        slug = slug or self.DEFAULT_PRODUCT
        return {
            "cart": str(self.cart.pk),
            "product_slug": slug,
            "quantity": quantity,
        }

    def add_item(self, slug=None, quantity=1):
        slug = slug or self.DEFAULT_PRODUCT
        if slug not in self.products:
            self.register_product(slug)
        return self.client.post(
            CART_ITEM_LIST_URL,
            self.item_payload(slug=slug, quantity=quantity),
            format="json",
        )

    def get_cart(self, uuid=None):
        return self.client.get(f"/api/v1/cart/{uuid or self.cart.pk}/")

    def assert_cart_price(self, expected):
        response = self.get_cart()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["price"], str(expected))

    def create_item(self, quantity=1, **overrides):
        defaults = {
            "product_id": uuid4(),
            "product_name": "Fender Stratocaster",
            "product_slug": "fender-stratocaster",
            "product_price": Decimal("1250.00"),
            "image_url": "https://cdn.example.com/img/fender-stratocaster.jpg",
            "quantity": quantity,
        }
        defaults.update(overrides)
        return CartItem.objects.create(cart=self.cart, **defaults)


class CartEndpointApiTestCase(CartApiMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.cart, _ = CartService.get_or_create_cart()
        self.item = self.create_item()


class CartItemApiTestCase(CartApiMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.cart, _ = CartService.get_or_create_cart()
