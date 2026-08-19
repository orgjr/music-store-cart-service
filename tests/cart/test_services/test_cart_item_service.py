from cart_item.models import CartItem
from services.cart_item_service import CartItemService
from tests.cart.test_services.base import CartServiceTestCase


class CartItemServiceAddOrIncreaseQuantityTest(CartServiceTestCase):
    def test_creates_item(self):
        item, created = self.add(1, "Gibson Les Paul", "1500.00")
        self.assertTrue(created)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(item.product_name, "Gibson Les Paul")

    def test_sets_item_price_on_creation(self):
        item, _ = self.add(1, "Gibson Les Paul", "1500.00", quantity=2)
        self.assertEqual(item.price, 3000)
        self.assertEqual(item.product_price, 1500)

    def test_sums_quantity_when_item_already_exists(self):
        self.add(1, "Gibson Les Paul", "1500.00")
        _, created = self.add(1, "Gibson Les Paul", "1500.00", quantity=2)
        item = self.get_item(1)
        self.assertFalse(created)
        self.assertEqual(item.quantity, 3)

    def test_updates_cart_price(self):
        self.add(1, "Gibson Les Paul", "1500.00")
        self.add(2, "Pearl Export", "250.00", quantity=2)
        self.assert_cart_price("2000.00")


class CartItemServiceIncrementTest(CartServiceTestCase):
    def test_increments_item_quantity(self):
        self.add(1, "Gibson Les Paul", "1500.00")
        item = self.get_item(1)
        CartItemService.increment(item.pk)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 2)

    def test_updates_cart_price(self):
        self.add(1, "Gibson Les Paul", "1500.00", quantity=2)
        item = self.get_item(1)
        CartItemService.increment(item.pk)
        self.assert_cart_price("4500.00")


class CartItemServiceDecrementTest(CartServiceTestCase):
    def setUp(self):
        super().setUp()
        self.add(1, "Gibson Les Paul", "1500.00", quantity=3)
        self.item = self.get_item(1)

    def test_decrements_quantity(self):
        CartItemService.decrement(self.item.pk)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 2)

    def test_removes_item_when_quantity_would_reach_zero(self):
        CartItemService.decrement(self.item.pk)
        CartItemService.decrement(self.item.pk)
        CartItemService.decrement(self.item.pk)
        self.assertFalse(CartItem.objects.filter(pk=self.item.pk).exists())

    def test_updates_cart_price(self):
        CartItemService.decrement(self.item.pk)
        self.assert_cart_price("3000.00")


class CartItemServiceClearTest(CartServiceTestCase):
    def setUp(self):
        super().setUp()
        self.add(1, "Gibson Les Paul", "1500.00")
        self.item = self.get_item(1)

    def test_deletes_item(self):
        CartItemService.clear(self.item.pk)
        self.assertFalse(CartItem.objects.filter(pk=self.item.pk).exists())

    def test_returns_none(self):
        item = CartItemService.clear(self.item.pk)
        self.assertEqual(item, None)

    def test_updates_cart_price(self):
        CartItemService.clear(self.item.pk)
        self.assert_cart_price("0.00")


class CartItemServiceUpdateQuantityTest(CartServiceTestCase):
    def test_sets_quantity(self):
        self.add(1, "Gibson Les Paul", "1500.00", quantity=2)
        item = self.get_item(1)
        CartItemService.update_quantity(item.pk, 3)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 3)

    def test_removes_item_when_quantity_is_zero(self):
        self.add(1, "Gibson Les Paul", "1500.00")
        item = self.get_item(1)
        CartItemService.update_quantity(item.pk, 0)
        self.assertFalse(CartItem.objects.filter(pk=item.pk).exists())

    def test_updates_cart_price(self):
        self.add(1, "Gibson Les Paul", "1500.00", quantity=2)
        item = self.get_item(1)
        CartItemService.update_quantity(item.pk, 4)
        self.assert_cart_price("6000.00")
