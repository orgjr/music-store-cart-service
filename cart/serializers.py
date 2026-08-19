from rest_framework import serializers

from cart.models import Cart
from cart_item.serializers import CartItemResponseSerializer


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ("customer",)


class CartResponseSerializer(serializers.ModelSerializer):
    items = CartItemResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"
