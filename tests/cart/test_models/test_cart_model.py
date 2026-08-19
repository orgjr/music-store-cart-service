from decimal import Decimal
from uuid import UUID, uuid4

from django.core.exceptions import ValidationError
from django.test import TestCase

from cart.models import Cart
from services.cart_service import CartService


class CartModelCreationTest(TestCase):
    def setUp(self):
        self.cart, _ = CartService.get_or_create_cart()

    def test_cart_gets_auto_generated_uuid(self):
        cart = Cart.objects.create()
        self.assertIsInstance(cart.uuid, UUID)
        self.assertEqual(cart.pk, cart.uuid)

    def test_cart_uuids_are_unique_across_instances(self):
        first, _ = CartService.get_or_create_cart()
        second, _ = CartService.get_or_create_cart(uuid4())
        self.assertNotEqual(first.pk, second.pk)

    def test_cart_price_defaults_to_zero(self):
        cart = Cart.objects.create()
        self.assertEqual(cart.price, Decimal("0.00"))

    def test_cart_customer_defaults_to_none(self):
        cart = Cart.objects.create()
        self.assertIsNone(cart.customer)

    def test_cart_can_be_created_with_a_customer(self):
        customer = uuid4()
        cart = Cart.objects.create(customer=customer)
        self.assertEqual(cart.customer, customer)

    def test_cart_customer_is_unique(self):
        customer = uuid4()
        Cart.objects.create(customer=customer)
        with self.assertRaises(ValidationError):
            Cart.objects.create(customer=customer)

    def test_cart_allows_multiple_instances_without_customer(self):
        Cart.objects.create()
        Cart.objects.create()
        self.assertEqual(Cart.objects.count(), 3)

    def test_cart_created_at_and_updated_at_are_set_on_creation(self):
        cart = Cart.objects.create()
        self.assertIsNotNone(cart.created_at)
        self.assertIsNotNone(cart.updated_at)

    def test_cart_updated_at_changes_when_cart_is_saved(self):
        cart = Cart.objects.create()
        original = cart.updated_at
        cart.price = Decimal("25.00")
        cart.save()
        self.assertGreater(cart.updated_at, original)

    def test_cart_str_contains_customer_and_uuid(self):
        self.assertEqual(
            str(self.cart), f"customer: {self.cart.customer}, cart: {self.cart.uuid}"
        )

    def test_cart_save_enforces_price_decimal_places(self):
        cart = Cart(price=Decimal("10.123"))
        with self.assertRaises(ValidationError):
            cart.save()

    def test_clean_generates_uuid_when_value_is_not_a_uuid(self):
        cart = Cart()
        cart.uuid = "not-a-uuid"
        cart.clean()
        self.assertIsInstance(cart.uuid, UUID)
