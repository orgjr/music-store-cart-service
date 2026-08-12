from decimal import Decimal

from cart.models import Cart, CartItem
from cart.services.cart_item_service import CartItemService
from cart.services.cart_service import CartService
from tests.cart.test_services.base import CartServiceTestCase


class CartServiceGetOrCreateCartTest(CartServiceTestCase):
    def test_creates_new_cart(self):
        cart, created = CartService.get_or_create_cart()
        self.assertTrue(created)
        self.assertIsNotNone(cart.pk)
        self.assertEqual(Cart.objects.count(), 2)

    def test_returns_existing_cart(self):
        same_cart, created = CartService.get_or_create_cart(self.cart.pk)
        self.assertFalse(created)
        self.assertEqual(same_cart.pk, self.cart.pk)
        self.assertEqual(Cart.objects.count(), 1)


class CartServiceUpdatePriceTest(CartServiceTestCase):
    def test_sums_unit_price_times_quantity(self):
        self.add(1, "Gibson Les Paul", "1500.00", quantity=2)
        self.add(2, "Pearl Export", "300.00")
        cart = CartService.update_price(self.cart.pk)
        self.assertEqual(cart.price, Decimal("3300.00"))

    def test_resets_price_when_cart_is_empty(self):
        self.add(1, "Gibson Les Paul", "1500.00")
        item = CartItem.objects.get(product_id=1)
        CartItemService.clear(self.cart.pk, item.pk)
        cart = CartService.update_price(self.cart.pk)
        self.assertEqual(cart.price, Decimal("0.00"))


class CartServiceClearTest(CartServiceTestCase):
    def setUp(self):
        super().setUp()
        self.add(1, "Gibson Les Paul", "1500.00")
        self.add(2, "Pearl Export", "250.00", quantity=2)

    def test_removes_all_items(self):
        CartService.clear(self.cart.pk)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_resets_cart_price(self):
        CartService.clear(self.cart.pk)
        self.assert_cart_price("0.00")
