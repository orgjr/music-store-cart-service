from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cart_item.models import CartItem
from cart_item.serializers import (
    CartItemResponseSerializer,
    CartItemSerializer,
)
from docs.api import cart_item_schema
from services.cart_item_service import CartItemService
from services.cart_service import CartService


@cart_item_schema
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all().order_by("-added_at")
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        cart = data.pop("cart")
        item, created = CartItemService.add_or_increase_quantity(
            cart, product_slug=data["product_slug"], quantity=data["quantity"]
        )
        CartService.update_price(cart.pk)
        item.refresh_from_db()
        return Response(
            CartItemResponseSerializer(item).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    def list(self, request):
        self.serializer_class = CartItemResponseSerializer
        [CartItemService.update_price(item.pk) for item in self.get_queryset()]
        return super().list(request)

    def retrieve(self, request, pk):
        self.serializer_class = CartItemResponseSerializer
        item = self.get_object()
        CartItemService.update_price(item.pk)
        return super().retrieve(request, pk)

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = False
        return self._update_item(request, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self._update_item(request, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        CartItemService.clear(instance.pk)
        CartService.update_price(instance.cart_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def increment(self, request, pk=None):
        instance = self.get_object()
        instance = CartItemService.increment(instance.pk)
        CartService.update_price(instance.cart_id)
        return Response(CartItemResponseSerializer(instance).data)

    @action(detail=True, methods=["post"])
    def decrement(self, request, pk=None):
        instance = self.get_object()
        instance = CartItemService.decrement(instance.pk)
        if not instance:
            return Response(status=status.HTTP_204_NO_CONTENT)
        CartService.update_price(instance.cart_id)
        return Response(CartItemResponseSerializer(instance).data)

    def _update_item(self, request, partial, **kwargs):
        instance = self.get_object()
        cart_id = instance.cart_id
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        quantity = data.pop("quantity", None)
        if quantity is not None:
            CartItemService.update_quantity(instance.pk, quantity)

        if data:
            CartItem.objects.filter(pk=instance.pk).update(**data)

        CartService.update_price(cart_id)

        if not CartItem.objects.filter(pk=instance.pk).exists():
            return Response(status=status.HTTP_204_NO_CONTENT)

        instance.refresh_from_db()
        return Response(CartItemResponseSerializer(instance).data)
