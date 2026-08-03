from cart.models import CartItem
from cart.services.cart_item_service import CartItemService
from tests.cart.test_services.base import CartServiceTestCase


class CartItemServiceAddOrUpdateQuantityTest(CartServiceTestCase):
    def test_creates_item(self):
        item, created = self.add(1, "Gibson Les Paul", "1500.00")
        self.assertTrue(created)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(item.product_name, "Gibson Les Paul")

    def test_sums_quantity_when_item_already_exists(self):
        self.add(1, "Gibson Les Paul", "1500.00")
        _, created = self.add(1, "Gibson Les Paul", "1500.00", quantity=2)
        item = CartItem.objects.get(product_id=1)
        self.assertFalse(created)
        self.assertEqual(item.quantity, 3)

    def test_updates_cart_price(self):
        self.add(1, "Gibson Les Paul", "1500.00")
        self.add(2, "Pearl Export", "250.00", quantity=2)
        self.assert_cart_price("2000.00")


class CartItemServiceAddTest(CartServiceTestCase):
    def test_increments_item_quantity(self):
        self.add(1, "Gibson Les Paul", "1500.00")
        CartItemService.add(self.cart.pk, 1)
        item = CartItem.objects.get(product_id=1)
        self.assertEqual(item.quantity, 2)

    def test_updates_cart_price(self):
        self.add(1, "Gibson Les Paul", "1500.00", quantity=2)
        CartItemService.add(self.cart.pk, 1)
        self.assert_cart_price("4500.00")


class CartItemServiceRemoveTest(CartServiceTestCase):
    def setUp(self):
        super().setUp()
        self.add(1, "Gibson Les Paul", "1500.00", quantity=3)

    def test_decrements_quantity(self):
        CartItemService.remove(self.cart.pk, 1)
        item = CartItem.objects.get(product_id=1)
        self.assertEqual(item.quantity, 2)

    def test_removes_item_when_quantity_would_reach_zero(self):
        CartItemService.remove(self.cart.pk, 1)
        CartItemService.remove(self.cart.pk, 1)
        CartItemService.remove(self.cart.pk, 1)
        self.assertFalse(CartItem.objects.filter(product_id=1).exists())

    def test_updates_cart_price(self):
        CartItemService.remove(self.cart.pk, 1)
        self.assert_cart_price("3000.00")


class CartItemServiceClearTest(CartServiceTestCase):
    def setUp(self):
        super().setUp()
        self.add(1, "Gibson Les Paul", "1500.00")

    def test_deletes_item(self):
        CartItemService.clear(self.cart.pk, 1)
        self.assertFalse(CartItem.objects.filter(product_id=1).exists())

    def test_returns_message_with_product_name(self):
        message = CartItemService.clear(self.cart.pk, 1)
        self.assertIn("Gibson Les Paul", message)

    def test_updates_cart_price(self):
        CartItemService.clear(self.cart.pk, 1)
        self.assert_cart_price("0.00")


class CartItemServiceUpdateQuantityTest(CartServiceTestCase):
    def test_increments_quantity_by_delta(self):
        self.add(1, "Gibson Les Paul", "1500.00", quantity=2)
        CartItemService.update_quantity(self.cart.pk, 1, 3)
        item = CartItem.objects.get(product_id=1)
        self.assertEqual(item.quantity, 5)

    def test_removes_item_when_delta_drops_quantity_below_one(self):
        self.add(1, "Gibson Les Paul", "1500.00")
        CartItemService.update_quantity(self.cart.pk, 1, -1)
        self.assertFalse(CartItem.objects.filter(product_id=1).exists())

    def test_updates_cart_price(self):
        self.add(1, "Gibson Les Paul", "1500.00", quantity=2)
        CartItemService.update_quantity(self.cart.pk, 1, 2)
        self.assert_cart_price("6000.00")