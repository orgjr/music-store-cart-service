from decimal import Decimal
from uuid import UUID

import requests
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime
from rest_framework.exceptions import ValidationError

from cart_item.models import CartItem


class CartItemService:
    @staticmethod
    def update_price(item_pk: UUID) -> CartItem:
        item = get_object_or_404(CartItem, pk=item_pk)
        item.price = item.product_price * item.quantity
        item.save(update_fields=["price"])
        item.refresh_from_db()
        return item

    @staticmethod
    def update_quantity(item_pk: UUID, quantity: int) -> CartItem:
        item = CartItem.objects.filter(pk=item_pk)
        item.update(quantity=quantity, updated_at=localtime())
        item = item.first()
        item.cart.save(update_fields=["updated_at"])
        if item.quantity == 0:
            return CartItemService.clear(item_pk)
        else:
            item = CartItemService.update_price(item_pk)

        return item

    @staticmethod
    def add_or_increase_quantity(
        cart: UUID, product_slug: str, quantity: int
    ) -> CartItem:
        response = requests.get(
            f"{settings.CATALOG_SERVICE_URL}/{product_slug}", timeout=5
        )
        product = response.json()
        try:
            item, created = CartItem.objects.get_or_create(
                cart=cart,
                product_id=product["uuid"],
                defaults={
                    "product_name": product["name"],
                    "product_slug": product["slug"],
                    "product_price": product["price"],
                    "image_url": product["image_url"],
                    "quantity": quantity,
                    "price": Decimal(product["price"]) * quantity,
                },
            )

            if not created:
                CartItem.objects.filter(pk=item.pk).update(
                    quantity=F("quantity") + quantity, updated_at=localtime()
                )
                item.cart.save(update_fields=["updated_at"])
                item = CartItemService.update_price(item.pk)

            return item, created
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

    @staticmethod
    def increment(item_pk: UUID) -> CartItem:
        item = CartItem.objects.filter(pk=item_pk)
        item.update(quantity=F("quantity") + 1, updated_at=localtime())
        item.first().cart.save(update_fields=["updated_at"])
        item = CartItemService.update_price(item_pk)
        return item

    @staticmethod
    def decrement(item_pk: UUID) -> CartItem | None:
        item = CartItem.objects.filter(pk=item_pk)

        if item.first().quantity == 1:
            return CartItemService.clear(item_pk)
        else:
            item.update(quantity=F("quantity") - 1, updated_at=localtime())
            item.first().cart.save(update_fields=["updated_at"])
            item = CartItemService.update_price(item_pk)

        return item

    @staticmethod
    def clear(item_pk):
        item = get_object_or_404(CartItem, pk=item_pk)
        item.delete()
