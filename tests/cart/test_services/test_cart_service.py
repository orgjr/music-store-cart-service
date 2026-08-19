from decimal import Decimal
from uuid import uuid4

from cart.models import Cart
from cart_item.models import CartItem
from services.cart_item_service import CartItemService
from services.cart_service import CartService
from tests.cart.test_services.base import CartServiceTestCase


class CartServiceGetOrCreateCartTest(CartServiceTestCase):
    def test_creates_new_cart_for_a_customer(self):
        cart, created = CartService.get_or_create_cart(uuid4())
        self.assertTrue(created)
        self.assertIsNotNone(cart.pk)
        self.assertEqual(Cart.objects.count(), 2)

    def test_returns_existing_anonymous_cart(self):
        same_cart, created = CartService.get_or_create_cart()
        self.assertFalse(created)
        self.assertEqual(same_cart.pk, self.cart.pk)
        self.assertEqual(Cart.objects.count(), 1)

    def test_returns_existing_cart_for_the_same_customer(self):
        customer = uuid4()
        first, _ = CartService.get_or_create_cart(customer)
        same_cart, created = CartService.get_or_create_cart(customer)
        self.assertFalse(created)
        self.assertEqual(same_cart.pk, first.pk)
        self.assertEqual(Cart.objects.count(), 2)


class CartServiceUpdatePriceTest(CartServiceTestCase):
    def test_sums_product_price_times_quantity(self):
        self.add(1, "Gibson Les Paul", "1500.00", quantity=2)
        self.add(2, "Pearl Export", "300.00")
        cart = CartService.update_price(self.cart.pk)
        self.assertEqual(cart.price, Decimal("3300.00"))

    def test_resets_price_when_cart_is_empty(self):
        self.add(1, "Gibson Les Paul", "1500.00")
        item = self.get_item(1)
        CartItemService.clear(item.pk)
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
