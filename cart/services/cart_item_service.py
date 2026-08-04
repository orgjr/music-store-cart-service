from django.db.models import F

from cart.models import Cart, CartItem
from cart.services.cart_service import CartService


class CartItemService:
    @staticmethod
    def update_quantity(cart_pk, product_id, quantity):
        cart = Cart.objects.get(pk=cart_pk)
        cart_item = cart.items.filter(product_id=product_id)
        if sum([cart_item.first().quantity, quantity]) < 1:
            CartItemService.clear(cart_pk, product_id)
        else:
            cart_item.update(quantity=F("quantity") + quantity)
        CartService.update_price(cart_pk)
        return cart_item

    @staticmethod
    def add_or_update_quantity(cart, data) -> CartItem:
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
                quantity=F("quantity") + data["quantity"]
            )
            cart_item.refresh_from_db()

        CartService.update_price(cart.pk)
        return cart_item, created

    @staticmethod
    def add(cart_pk, product_id):
        try:
            cart = Cart.objects.get(pk=cart_pk)
        except Cart.DoesNotExist:
            raise Cart.DoesNotExist("Cart was not created yet")
        cart_item = cart.items.filter(product_id=product_id)
        cart_item.update(quantity=F("quantity") + 1)
        CartService.update_price(cart_pk)
        return f"{cart_item} increased"

    @staticmethod
    def remove(cart_pk, product_id):
        try:
            cart = Cart.objects.get(pk=cart_pk)
        except Cart.DoesNotExist:
            raise Cart.DoesNotExist("Cart was not created yet")
        cart_item = cart.items.filter(product_id=product_id)
        if cart_item.first().quantity == 1:
            CartItemService.clear(cart_pk, product_id)
        else:
            cart_item.update(quantity=F("quantity") - 1)
        CartService.update_price(cart_pk)
        return f"{cart_item} decreased"

    @staticmethod
    def clear(cart_pk, product_id) -> str:
        try:
            cart = Cart.objects.get(pk=cart_pk)
        except Cart.DoesNotExist:
            raise Cart.DoesNotExist("Cart was not created yet")
        item = cart.items.get(product_id=product_id)
        item.delete()
        CartService.update_price(cart_pk)
        return f"{item} removed"
