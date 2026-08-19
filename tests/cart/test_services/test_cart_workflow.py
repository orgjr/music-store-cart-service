from cart.models import Cart
from cart_item.models import CartItem
from services.cart_item_service import CartItemService
from services.cart_service import CartService
from tests.cart.test_services.base import CartServiceTestCase


class CartServiceFunctionalTest(CartServiceTestCase):
    def test_full_cart_lifecycle(self):
        self.add(1, "Gibson Les Paul", "1500.00")
        self.add(2, "Pearl Export", "250.00")
        self.assert_cart_price("1750.00")

        item1 = self.get_item(1)
        CartItemService.increment(item1.pk)
        self.assert_cart_price("3250.00")

        item1.refresh_from_db()
        item2 = self.get_item(2)
        CartItemService.decrement(item1.pk)
        CartItemService.decrement(item2.pk)
        self.assert_cart_price("1500.00")

        item1.refresh_from_db()
        CartItemService.decrement(item1.pk)
        self.assert_cart_price("0.00")
        self.assertEqual(CartItem.objects.count(), 0)
        self.assertTrue(Cart.objects.filter(pk=self.cart.pk).exists())

    def test_cart_can_be_reused_after_being_emptied(self):
        self.add(1, "Gibson Les Paul", "1500.00")
        CartService.clear(self.cart.pk)
        self.add(2, "Pearl Export", "250.00")
        self.assert_cart_price("250.00")
        self.assertEqual(CartItem.objects.count(), 1)

    def test_multiple_products_share_single_cart_and_price(self):
        expected = 0
        for product_id, price in [(1, "1500.00"), (2, "250.00"), (3, "775.00")]:
            self.add(product_id, f"product-{product_id}", price)
            expected += float(price)
            self.assert_cart_price(f"{expected:.2f}")

    def test_same_product_added_twice_keeps_one_item_with_summed_quantity(self):
        self.add(1, "Gibson Les Paul", "1500.00")
        self.add(1, "Gibson Les Paul", "1500.00", quantity=3)
        items = CartItem.objects.filter(cart=self.cart)
        self.assertEqual(items.count(), 1)
        self.assertEqual(items.get().quantity, 4)
