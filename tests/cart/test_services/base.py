from decimal import Decimal

from django.test import TestCase

from cart.services.cart_item_service import CartItemService
from cart.services.cart_service import CartService


class CartServiceTestCase(TestCase):
    def setUp(self):
        self.cart, _ = CartService.get_or_create_cart()

    def item_data(self, product_id, name, price, quantity=1):
        return {
            "product_id": product_id,
            "product_name": name,
            "product_slug": name.replace(" ", "-").lower(),
            "unit_price": Decimal(str(price)),
            "image_url": f"{name}/img/",
            "quantity": quantity,
        }

    def add(self, product_id, name, price, quantity=1):
        return CartItemService.add_or_update_quantity(
            self.cart, self.item_data(product_id, name, price, quantity)
        )

    def assert_cart_price(self, price):
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.price, Decimal(str(price)))