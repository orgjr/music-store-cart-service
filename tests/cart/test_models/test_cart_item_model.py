from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from cart.models import Cart, CartItem
from tests.cart.test_models.base import CartItemTestCase


class CartItemModelCreationTest(CartItemTestCase, TestCase):
    def test_cart_item_creation_round_trip(self):
        item = self.create_item(
            product_id=7, name="Roland TD-17", price="4990.00", quantity=3
        )
        self.assertEqual(item.cart, self.cart)
        self.assertEqual(item.product_id, 7)
        self.assertEqual(item.product_name, "Roland TD-17")
        self.assertEqual(item.product_slug, "roland-td-17")
        self.assertEqual(item.unit_price, Decimal("4990.00"))
        self.assertEqual(item.image_url, "Roland TD-17/img/")
        self.assertEqual(item.quantity, 3)

    def test_cart_item_is_exposed_through_cart_items_related_name(self):
        self.create_item()
        self.assertEqual(self.cart.items.count(), 1)

    def test_cart_item_added_at_is_set_on_creation(self):
        item = self.create_item()
        self.assertIsNotNone(item.added_at)

    def test_cart_item_str_returns_product_name(self):
        item = self.create_item(name="Gibson Les Paul")
        self.assertEqual(str(item), "Gibson Les Paul")

    def test_cart_item_quantity_must_be_at_least_one(self):
        item = CartItem(**self.item_data(quantity=0))
        with self.assertRaises(ValidationError):
            item.save()

    def test_cart_item_product_id_must_be_positive(self):
        item = CartItem(**self.item_data(product_id=0))
        with self.assertRaises(ValidationError):
            item.save()

    def test_cart_item_product_id_cannot_be_negative(self):
        item = CartItem(**self.item_data(product_id=-1))
        with self.assertRaises(ValidationError):
            item.save()

    def test_cart_item_quantity_cannot_be_negative(self):
        item = CartItem(**self.item_data(quantity=-1))
        with self.assertRaises(ValidationError):
            item.save()

    def test_cart_item_negative_values_rejected_at_database_level(self):
        with self.assertRaises(IntegrityError):
            CartItem.objects.bulk_create(
                [
                    CartItem(
                        cart=self.cart,
                        product_id=-1,
                        product_name="Gibson Les Paul",
                        product_slug="gibson-les-paul",
                        unit_price=Decimal("1500.00"),
                        image_url="Gibson Les Paul/img/",
                        quantity=1,
                    )
                ]
            )
        with self.assertRaises(IntegrityError):
            CartItem.objects.bulk_create(
                [
                    CartItem(
                        cart=self.cart,
                        product_id=2,
                        product_name="Pearl Export",
                        product_slug="pearl-export",
                        unit_price=Decimal("250.00"),
                        image_url="Pearl Export/img/",
                        quantity=-1,
                    )
                ]
            )

    def test_cart_item_unit_price_enforces_two_decimals(self):
        item = CartItem(**self.item_data(price="10.123"))
        with self.assertRaises(ValidationError):
            item.save()

    def test_cart_item_product_slug_must_be_a_valid_slug(self):
        item = CartItem(**self.item_data())
        item.product_slug = "not a valid slug!"
        with self.assertRaises(ValidationError):
            item.save()

    def test_cart_item_enforces_field_max_lengths(self):
        item = CartItem(**self.item_data())
        item.product_name = "x" * 101
        with self.assertRaises(ValidationError):
            item.save()
        item = CartItem(**self.item_data())
        item.image_url = "x" * 251
        with self.assertRaises(ValidationError):
            item.save()

    def test_cart_item_requires_a_cart(self):
        item = CartItem(
            product_id=1,
            product_name="Gibson Les Paul",
            product_slug="gibson-les-paul",
            unit_price=Decimal("1500.00"),
            image_url="Gibson Les Paul/img/",
            quantity=1,
        )
        with self.assertRaises(ValidationError):
            item.save()

    def test_cart_item_requires_a_cart_at_database_level(self):
        with self.assertRaises(IntegrityError):
            CartItem.objects.bulk_create(
                [
                    CartItem(
                        product_id=1,
                        product_name="Gibson Les Paul",
                        product_slug="gibson-les-paul",
                        unit_price=Decimal("1500.00"),
                        image_url="Gibson Les Paul/img/",
                        quantity=1,
                    )
                ]
            )

    def test_one_product_per_cart_constraint(self):
        self.create_item(product_id=1)
        with self.assertRaises(ValidationError):
            self.create_item(product_id=1)

    def test_one_product_per_cart_constraint_at_database_level(self):
        self.create_item(product_id=1)
        item = CartItem(
            cart=self.cart,
            product_id=1,
            product_name="Gibson Les Paul",
            product_slug="gibson-les-paul",
            unit_price=Decimal("1500.00"),
            image_url="Gibson Les Paul/img/",
            quantity=1,
        )
        with self.assertRaises(IntegrityError):
            CartItem.objects.bulk_create([item])

    def test_same_product_allowed_in_different_carts(self):
        other = Cart.objects.create()
        self.create_item(product_id=1)
        CartItem.objects.create(**self.item_data(product_id=1, cart=other))
        self.assertEqual(CartItem.objects.count(), 2)

    def test_different_products_allowed_in_same_cart(self):
        self.create_item(product_id=1)
        self.create_item(product_id=2)
        self.assertEqual(CartItem.objects.count(), 2)

    def test_deleting_cart_cascades_to_its_items(self):
        self.create_item()
        self.create_item(product_id=2)
        self.cart.delete()
        self.assertEqual(CartItem.objects.count(), 0)
        self.assertFalse(Cart.objects.filter(pk=self.cart.pk).exists())