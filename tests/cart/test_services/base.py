from decimal import Decimal

from django.test import TestCase

from cart_item.models import CartItem
from services.cart_item_service import CartItemService
from services.cart_service import CartService
from tests.base import ProductServiceMockMixin, product_uuid


class CartServiceTestCase(ProductServiceMockMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.cart, _ = CartService.get_or_create_cart()

    def register_product(self, product_id, name, price):
        slug = name.replace(" ", "-").lower()
        return super().register_product(
            slug, name=name, price=price, product_id=product_uuid(product_id)
        )

    def add(self, product_id, name, price, quantity=1):
        product = self.register_product(product_id, name, price)
        return CartItemService.add_or_increase_quantity(
            self.cart, product["slug"], quantity
        )

    def get_item(self, product_id):
        return CartItem.objects.get(product_id=product_uuid(product_id))

    def assert_cart_price(self, price):
        CartService.update_price(self.cart.pk)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.price, Decimal(str(price)))
