from decimal import Decimal

from django.test import TestCase

from cart.models import CartItem
from cart.services.cart_service import CartService


class CartItemDataMixin:
    def item_data(
        self,
        product_id=1,
        name="Gibson Les Paul",
        price="1500.00",
        quantity=1,
        cart=None,
    ):
        return {
            "cart": cart or self.cart,
            "product_id": product_id,
            "product_name": name,
            "product_slug": name.replace(" ", "-").lower(),
            "unit_price": Decimal(str(price)),
            "image_url": f"{name}/img/",
            "quantity": quantity,
        }

    def create_item(self, **overrides):
        return CartItem.objects.create(**self.item_data(**overrides))


class CartItemTestCase(CartItemDataMixin, TestCase):
    def setUp(self):
        self.cart, _ = CartService.get_or_create_cart()