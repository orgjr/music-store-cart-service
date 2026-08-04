from cart.models import Cart


class CartService:
    @staticmethod
    def get_or_create_cart(cart_pk=None):
        cart, created = Cart.objects.get_or_create(pk=cart_pk)
        return cart, created

    @staticmethod
    def update_price(cart_pk):
        cart = Cart.objects.get(pk=cart_pk)
        price = sum([item.unit_price * item.quantity for item in cart.items.all()])
        cart.price = price
        cart.save(update_fields=["price"])
        return cart

    @staticmethod
    def clear(cart_pk):
        try:
            cart = Cart.objects.get(pk=cart_pk)
        except Cart.DoesNotExist:
            raise Cart.DoesNotExist("Cart was not created yet")
        cart_items = cart.items.all()
        cart_items.delete()
        CartService.update_price(cart_pk)
        return f"{cart} removed"
