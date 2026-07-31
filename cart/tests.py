from decimal import Decimal

from django.test import TestCase

from cart.models import Cart, CartItem
from cart.services.cart_item_service import CartItemService
from cart.services.cart_service import CartService


class CartServiceTestCase(TestCase):
    def setUp(self):
        self.cart, _ = CartService.get_or_create_cart()

    def item_data(self, product_id, name, price, quantity=1):
        return {
            "cart": self.cart,
            "product_id": product_id,
            "product_name": name,
            "product_slug": name,
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
        self.add(1, "chocolate", "10.00", quantity=2)
        self.add(2, "cookies", "3.00")
        cart = CartService.update_price(self.cart.pk)
        self.assertEqual(cart.price, Decimal("23.00"))

    def test_resets_price_when_cart_is_empty(self):
        self.add(1, "chocolate", "10.00")
        CartItemService.clear(self.cart.pk, 1)
        cart = CartService.update_price(self.cart.pk)
        self.assertEqual(cart.price, Decimal("0.00"))


class CartServiceClearTest(CartServiceTestCase):
    def setUp(self):
        super().setUp()
        self.add(1, "chocolate", "10.00")
        self.add(2, "cookies", "2.50", quantity=2)

    def test_removes_all_items(self):
        CartService.clear(self.cart.pk)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_resets_cart_price(self):
        CartService.clear(self.cart.pk)
        self.assert_cart_price("0.00")


class CartItemServiceAddOrUpdateQuantityTest(CartServiceTestCase):
    def test_creates_item(self):
        item, created = self.add(1, "chocolate", "10.00")
        self.assertTrue(created)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(item.product_name, "chocolate")

    def test_sums_quantity_when_item_already_exists(self):
        self.add(1, "chocolate", "10.00")
        _, created = self.add(1, "chocolate", "10.00", quantity=2)
        item = CartItem.objects.get(product_id=1)
        self.assertFalse(created)
        self.assertEqual(item.quantity, 3)

    def test_updates_cart_price(self):
        self.add(1, "chocolate", "10.00")
        self.add(2, "cookies", "2.50", quantity=2)
        self.assert_cart_price("15.00")


class CartItemServiceAddTest(CartServiceTestCase):
    def test_increments_item_quantity(self):
        self.add(1, "chocolate", "10.00")
        CartItemService.add(self.cart.pk, 1)
        item = CartItem.objects.get(product_id=1)
        self.assertEqual(item.quantity, 2)

    def test_updates_cart_price(self):
        self.add(1, "chocolate", "10.00", quantity=2)
        CartItemService.add(self.cart.pk, 1)
        self.assert_cart_price("30.00")


class CartItemServiceRemoveTest(CartServiceTestCase):
    def setUp(self):
        super().setUp()
        self.add(1, "chocolate", "10.00", quantity=3)

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
        self.assert_cart_price("20.00")


class CartItemServiceClearTest(CartServiceTestCase):
    def setUp(self):
        super().setUp()
        self.add(1, "chocolate", "10.00")

    def test_deletes_item(self):
        CartItemService.clear(self.cart.pk, 1)
        self.assertFalse(CartItem.objects.filter(product_id=1).exists())

    def test_returns_message_with_product_name(self):
        message = CartItemService.clear(self.cart.pk, 1)
        self.assertIn("chocolate", message)

    def test_updates_cart_price(self):
        CartItemService.clear(self.cart.pk, 1)
        self.assert_cart_price("0.00")


class CartItemServiceUpdateQuantityTest(CartServiceTestCase):
    def test_increments_quantity_by_delta(self):
        self.add(1, "chocolate", "10.00", quantity=2)
        CartItemService.update_quantity(self.cart.pk, 1, 3)
        item = CartItem.objects.get(product_id=1)
        self.assertEqual(item.quantity, 5)

    def test_removes_item_when_delta_drops_quantity_below_one(self):
        self.add(1, "chocolate", "10.00")
        CartItemService.update_quantity(self.cart.pk, 1, -1)
        self.assertFalse(CartItem.objects.filter(product_id=1).exists())

    def test_updates_cart_price(self):
        self.add(1, "chocolate", "10.00", quantity=2)
        CartItemService.update_quantity(self.cart.pk, 1, 2)
        self.assert_cart_price("40.00")


class CartServiceFunctionalTest(CartServiceTestCase):
    def test_full_cart_lifecycle(self):
        self.add(1, "chocolate", "10.00")
        self.add(2, "cookies", "2.50")
        self.assert_cart_price("12.50")

        CartItemService.add(self.cart.pk, 1)
        self.assert_cart_price("22.50")

        CartItemService.remove(self.cart.pk, 1)
        CartItemService.remove(self.cart.pk, 2)
        self.assert_cart_price("10.00")

        CartItemService.remove(self.cart.pk, 1)
        self.assert_cart_price("0.00")
        self.assertEqual(CartItem.objects.count(), 0)
        self.assertTrue(Cart.objects.filter(pk=self.cart.pk).exists())

    def test_cart_can_be_reused_after_being_emptied(self):
        self.add(1, "chocolate", "10.00")
        CartService.clear(self.cart.pk)
        self.add(2, "cookies", "2.50")
        self.assert_cart_price("2.50")
        self.assertEqual(CartItem.objects.count(), 1)

    def test_multiple_products_share_single_cart_and_price(self):
        expected = Decimal("0.00")
        for product_id, price in [(1, "10.00"), (2, "2.50"), (3, "7.75")]:
            self.add(product_id, f"product-{product_id}", price)
            expected += Decimal(price)
            self.assert_cart_price(str(expected))

    def test_same_product_added_twice_keeps_one_item_with_summed_quantity(self):
        self.add(1, "chocolate", "10.00")
        self.add(1, "chocolate", "10.00", quantity=3)
        items = CartItem.objects.filter(cart=self.cart)
        self.assertEqual(items.count(), 1)
        self.assertEqual(items.get().quantity, 4)
