from decimal import Decimal
from uuid import uuid4

from django.test import TestCase

from cart_item.models import CartItem
from services.cart_service import CartService


class CartItemDataMixin:
    def item_data(
        self,
        product_id=None,
        name="Gibson Les Paul",
        price="1500.00",
        quantity=1,
        cart=None,
    ):
        slug = name.replace(" ", "-").lower()
        return {
            "cart": cart or self.cart,
            "product_id": product_id or uuid4(),
            "product_name": name,
            "product_slug": slug,
            "product_price": Decimal(str(price)),
            "image_url": f"https://cdn.example.com/img/{slug}.jpg",
            "quantity": quantity,
        }

    def create_item(self, **overrides):
        return CartItem.objects.create(**self.item_data(**overrides))


class CartItemTestCase(CartItemDataMixin, TestCase):
    def setUp(self):
        self.cart, _ = CartService.get_or_create_cart()
