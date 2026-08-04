from drf_spectacular.utils import extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response

from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer
from cart.services.cart_item_service import CartItemService
from cart.services.cart_service import CartService
from docs.api.cart import (
    cart_clear,
    cart_create,
    cart_list,
    cart_partial_update,
    cart_retrieve,
    cart_update,
    item_create,
    item_decrement,
    item_destroy,
    item_increment,
    item_list,
    item_partial_update,
    item_retrieve,
    item_update,
)


@extend_schema_view(
    list=cart_list.list_schema,
    create=cart_create.create_schema,
    retrieve=cart_retrieve.retrieve_schema,
    update=cart_update.update_schema,
    partial_update=cart_partial_update.partial_update_schema,
    clear=cart_clear.clear_schema,
)
class CartViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
):
    queryset = Cart.objects.all().order_by("-created_at")
    serializer_class = CartSerializer
    lookup_value_regex = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

    def create(self, request, *args, **kwargs):
        cart, _ = CartService.get_or_create_cart()
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], url_path="items", url_name="clear")
    def clear(self, request, pk=None):
        cart = self.get_object()
        CartService.clear(cart.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    list=item_list.list_schema,
    create=item_create.create_schema,
    retrieve=item_retrieve.retrieve_schema,
    update=item_update.update_schema,
    partial_update=item_partial_update.partial_update_schema,
    destroy=item_destroy.destroy_schema,
    increment=item_increment.increment_schema,
    decrement=item_decrement.decrement_schema,
)
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all().order_by("-added_at")
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        cart = data.pop("cart")
        item, created = CartItemService.add_or_update_quantity(cart, data)
        return Response(
            self.get_serializer(item).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = False
        return self._update_item(request, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self._update_item(request, **kwargs)

    def _update_item(self, request, partial, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        quantity = data.pop("quantity", None)
        if quantity is not None:
            CartItemService.update_quantity(
                instance.cart_id, instance.product_id, quantity
            )

        if data:
            CartItem.objects.filter(pk=instance.pk).update(**data)
            CartService.update_price(instance.cart_id)

        if not CartItem.objects.filter(pk=instance.pk).exists():
            return Response(status=status.HTTP_204_NO_CONTENT)

        instance.refresh_from_db()
        return Response(self.get_serializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        CartItemService.clear(instance.cart_id, instance.product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def increment(self, request, pk=None):
        instance = self.get_object()
        CartItemService.add(instance.cart_id, instance.product_id)
        instance.refresh_from_db()
        return Response(self.get_serializer(instance).data)

    @action(detail=True, methods=["post"])
    def decrement(self, request, pk=None):
        instance = self.get_object()
        CartItemService.remove(instance.cart_id, instance.product_id)
        if CartItem.objects.filter(pk=instance.pk).exists():
            instance.refresh_from_db()
            return Response(self.get_serializer(instance).data)
        return Response(status=status.HTTP_204_NO_CONTENT)
