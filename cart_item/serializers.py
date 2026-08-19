from rest_framework import serializers

from cart_item.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(validators=[])

    class Meta:
        model = CartItem
        fields = ("cart", "product_slug", "quantity")

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Quantity must be at least 1 when adding an item."
            )
        return value


class CartItemResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
