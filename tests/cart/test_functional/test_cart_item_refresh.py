from decimal import Decimal
from uuid import uuid4

from rest_framework import status
from rest_framework.test import APITestCase

from cart.models import Cart
from cart_item.models import CartItem
from tests.base import product_uuid

API_ROOT = "/api/v1"


class CartItemReadRefreshFunctionalTests(APITestCase):
    """Verifies that read endpoints surface the *current* state of carts and
    cart items.

    Items are registered through a flow that intentionally does NOT refresh
    the database: the `price` snapshot is never recalculated, so it stays out
    of sync with `product_price * quantity`. A correct read endpoint must
    recalculate prices on the fly (or the stored state must already be
    consistent)."""

    def setUp(self):
        self.cart = Cart.objects.create()

    def register_stale_item(
        self,
        product_id=1,
        name="Gibson Les Paul",
        unit_price="100.00",
        quantity=2,
    ):
        """Registers an item whose `price` snapshot is deliberately stale.

        `product_price * quantity` is 200.00, but the stored `price` stays at
        the default 0.00, simulating an item that was created by a flow which
        does not refresh the cart state in the database."""
        slug = name.replace(" ", "-").lower()
        return CartItem.objects.create(
            cart=self.cart,
            product_id=product_uuid(product_id),
            product_name=name,
            product_slug=slug,
            product_price=Decimal(unit_price),
            quantity=quantity,
            price=Decimal("0.00"),
        )

    def register_item_with_stale_quantity(self, product_id=1, quantity=3):
        """Creates a consistent item, then changes its quantity directly in the
        database without refreshing the `price` snapshot."""
        item = CartItem.objects.create(
            cart=self.cart,
            product_id=product_uuid(product_id),
            product_name="Gibson Les Paul",
            product_slug="gibson-les-paul",
            product_price=Decimal("100.00"),
            quantity=1,
            price=Decimal("100.00"),
        )
        CartItem.objects.filter(pk=item.pk).update(quantity=quantity)
        return item

    def cart_list_url(self):
        return f"{API_ROOT}/cart/"

    def cart_detail_url(self):
        return f"{API_ROOT}/cart/{self.cart.pk}/"

    def item_list_url(self):
        return f"{API_ROOT}/cart/items/"

    def item_detail_url(self, item):
        return f"{API_ROOT}/cart/items/{item.pk}/"

    # --- cart list ---------------------------------------------------------

    def test_cart_list_recalculates_item_prices(self):
        self.register_stale_item()
        response = self.client.get(self.cart_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertEqual(body["results"][0]["items"][0]["price"], "200.00")

    def test_cart_list_recalculates_cart_total(self):
        self.register_stale_item()
        response = self.client.get(self.cart_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"][0]["price"], "200.00")

    def test_cart_list_with_no_items_returns_zero_total(self):
        response = self.client.get(self.cart_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"][0]["price"], "0.00")

    # --- cart retrieve -----------------------------------------------------

    def test_cart_retrieve_recalculates_item_prices(self):
        self.register_stale_item()
        response = self.client.get(self.cart_detail_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["items"][0]["price"], "200.00")

    def test_cart_retrieve_recalculates_cart_total(self):
        self.register_stale_item()
        response = self.client.get(self.cart_detail_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["price"], "200.00")

    def test_cart_retrieve_with_no_items_returns_zero_total(self):
        response = self.client.get(self.cart_detail_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["price"], "0.00")

    def test_cart_retrieve_unknown_cart_returns_404(self):
        response = self.client.get(f"{API_ROOT}/cart/{uuid4()}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # --- cart item list ----------------------------------------------------

    def test_cart_item_list_reflects_updated_prices(self):
        self.register_stale_item()
        response = self.client.get(self.item_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertEqual(body["results"][0]["price"], "200.00")

    def test_cart_item_list_with_no_items_returns_empty(self):
        response = self.client.get(self.item_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 0)

    # --- cart item retrieve ------------------------------------------------

    def test_cart_item_retrieve_reflects_updated_price(self):
        item = self.register_stale_item()
        response = self.client.get(self.item_detail_url(item))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["price"], "200.00")

    def test_cart_item_retrieve_reflects_quantity_change(self):
        item = self.register_item_with_stale_quantity()
        response = self.client.get(self.item_detail_url(item))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["price"], "300.00")

    def test_cart_item_retrieve_unknown_item_returns_404(self):
        response = self.client.get(f"{API_ROOT}/cart/items/{uuid4()}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
