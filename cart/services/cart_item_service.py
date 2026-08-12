from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import F
from django.utils.timezone import localtime
from rest_framework.exceptions import ValidationError

from cart.models import Cart, CartItem
from cart.services.cart_service import CartService


class CartItemService:
    @staticmethod
    def update_quantity(cart_pk, item_pk, quantity):
        cart = Cart.objects.get(pk=cart_pk)
        cart_item = cart.items.filter(pk=item_pk)
        cart_item.update(quantity=quantity, added_at=localtime())

        cart_item = cart_item.first()
        cart_item.refresh_from_db()

        if cart_item.quantity == 0:
            CartItemService.clear(cart_pk, item_pk)

        CartService.update_price(cart_pk)
        return cart_item

    @staticmethod
    def add_or_increase_quantity(cart, data) -> CartItem:
        try:
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product_id=data["product_id"],
                defaults={
                    "product_name": data["product_name"],
                    "product_slug": data["product_slug"],
                    "unit_price": data["unit_price"],
                    "image_url": data["image_url"],
                    "quantity": data["quantity"],
                },
            )

            if not created:
                CartItem.objects.filter(pk=cart_item.pk).update(
                    quantity=F("quantity") + data["quantity"], added_at=localtime()
                )
                cart_item.refresh_from_db()

            CartService.update_price(cart.pk)
            return cart_item, created
        except DjangoValidationError as e:
            raise ValidationError(e)

    @staticmethod
    def increment(cart_pk, item_pk):
        try:
            cart = Cart.objects.get(pk=cart_pk)
        except Cart.DoesNotExist:
            raise Cart.DoesNotExist("Cart was not created yet")
        cart_item = cart.items.filter(pk=item_pk)
        cart_item.update(quantity=F("quantity") + 1, added_at=localtime())
        cart_item = cart_item.first()
        cart_item.refresh_from_db()
        CartService.update_price(cart_pk)
        return cart_item

    @staticmethod
    def decrement(cart_pk, item_pk):
        try:
            cart = Cart.objects.get(pk=cart_pk)
        except Cart.DoesNotExist:
            raise Cart.DoesNotExist("Cart was not created yet")
        cart_item = cart.items.filter(pk=item_pk)
        if cart_item.first().quantity == 1:
            CartItemService.clear(cart_pk, item_pk)
        else:
            cart_item.update(quantity=F("quantity") - 1, added_at=localtime())

        cart_item = cart_item.first()
        if cart_item:
            cart_item.refresh_from_db()

        CartService.update_price(cart_pk)
        return cart_item

    @staticmethod
    def clear(cart_pk, item_pk) -> str:
        try:
            cart = Cart.objects.get(pk=cart_pk)
        except Cart.DoesNotExist:
            raise Cart.DoesNotExist("Cart was not created yet")
        cart_item = cart.items.get(pk=item_pk)
        cart_item.delete()
        CartService.update_price(cart_pk)
        return cart_item
