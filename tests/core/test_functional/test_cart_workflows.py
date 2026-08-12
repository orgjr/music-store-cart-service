from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cart.models import Cart, CartItem
from tests.core.test_functional.base import ITEM_PAYLOAD

API_ROOT = "/api/v1"


class CartWorkflowFunctionalTests(APITestCase):
    def setUp(self):
        self.cart = Cart.objects.create()
        self.cart_payload = dict(ITEM_PAYLOAD, cart=str(self.cart.pk))

    def get_cart(self):
        return self.client.get(f"{API_ROOT}/cart/{self.cart.pk}/")

    def assert_cart_price(self, expected):
        response = self.get_cart()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["price"], str(expected))

    def test_full_shopping_workflow_through_the_public_api(self):
        index = self.client.get(API_ROOT + "/")
        self.assertEqual(index.status_code, status.HTTP_200_OK)
        health = self.client.get(API_ROOT + "/health/")
        self.assertEqual(health.status_code, status.HTTP_200_OK)

        add = self.client.post(
            f"{API_ROOT}/cart/items/", self.cart_payload, format="json"
        )
        self.assertEqual(add.status_code, status.HTTP_201_CREATED)
        item_id = add.json()["id"]
        self.assert_cart_price(Decimal("1250.00"))

        duplicate = self.client.post(
            f"{API_ROOT}/cart/items/", self.cart_payload, format="json"
        )
        self.assertEqual(duplicate.status_code, status.HTTP_200_OK)
        self.assertEqual(duplicate.json()["quantity"], 2)
        self.assert_cart_price(Decimal("2500.00"))

        bump = self.client.patch(
            f"{API_ROOT}/cart/items/{item_id}/",
            {"quantity": 3},
            format="json",
        )
        self.assertEqual(bump.status_code, status.HTTP_200_OK)
        self.assertEqual(bump.json()["quantity"], 3)
        self.assert_cart_price(Decimal("3750.00"))

        inc = self.client.post(f"{API_ROOT}/cart/items/{item_id}/increment/")
        self.assertEqual(inc.status_code, status.HTTP_200_OK)
        self.assertEqual(inc.json()["quantity"], 4)

        dec = self.client.post(f"{API_ROOT}/cart/items/{item_id}/decrement/")
        self.assertEqual(dec.status_code, status.HTTP_200_OK)
        self.assertEqual(dec.json()["quantity"], 3)

        self.assert_cart_price(Decimal("3750.00"))

    def test_cart_is_cleared_through_delete_items_route(self):
        self.client.post(f"{API_ROOT}/cart/items/", self.cart_payload, format="json")
        self.assert_cart_price(Decimal("1250.00"))
        self.assertEqual(CartItem.objects.filter(cart=self.cart).count(), 1)

        clear = self.client.delete(reverse("cart-clear", args=[self.cart.pk]))
        self.assertEqual(clear.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.filter(cart=self.cart).count(), 0)
        self.assert_cart_price(Decimal("0.00"))

    def test_item_is_deleted_and_cart_price_recalculated(self):
        self.client.post(f"{API_ROOT}/cart/items/", self.cart_payload, format="json")
        item = CartItem.objects.get(cart=self.cart)
        response = self.client.delete(reverse("cart-item-detail", args=[item.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(pk=item.pk).exists())
        self.assert_cart_price(Decimal("0.00"))

    def test_cart_list_is_paginated_with_carts(self):
        self.client.post(f"{API_ROOT}/cart/items/", self.cart_payload, format="json")
        response = self.client.get(f"{API_ROOT}/cart/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("count", body)
        self.assertIn("results", body)
        self.assertEqual(body["count"], 1)
        self.assertEqual(body["results"][0]["uuid"], str(self.cart.pk))
        self.assertEqual(body["results"][0]["price"], "1250.00")

    def test_two_carts_keep_independent_prices(self):
        self.client.post(f"{API_ROOT}/cart/items/", self.cart_payload, format="json")
        other = Cart.objects.create()
        other_payload = dict(
            ITEM_PAYLOAD,
            cart=str(other.pk),
            product_id=99,
            unit_price="99.90",
        )
        self.client.post(f"{API_ROOT}/cart/items/", other_payload, format="json")

        self.assert_cart_price(Decimal("1250.00"))
        other_response = self.client.get(f"{API_ROOT}/cart/{other.pk}/")
        self.assertEqual(other_response.json()["price"], "99.90")

        self.client.delete(reverse("cart-clear", args=[self.cart.pk]))
        self.assert_cart_price(Decimal("0.00"))
        other_response = self.client.get(f"{API_ROOT}/cart/{other.pk}/")
        self.assertEqual(other_response.json()["price"], "99.90")
