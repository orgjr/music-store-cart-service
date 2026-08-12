from typing import ClassVar

from rest_framework import serializers

from cart.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = "__all__"
        read_only_fields = ("id", "added_at")
        validators: ClassVar = []

    def validate_quantity(self, value):
        if self.instance is None and value < 0:
            raise serializers.ValidationError(
                "Quantity must be at least 1 when adding an item."
            )
        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = (
            "uuid",
            "customer",
            "price",
            "items",
            "created_at",
            "updated_at",
        )
