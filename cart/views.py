from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.response import Response

from cart.models import Cart
from cart.serializers import (
    CartResponseSerializer,
    CartSerializer,
)
from docs.api import cart_schema
from services.cart_item_service import CartItemService
from services.cart_service import CartService


@cart_schema
class CartViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
):
    queryset = Cart.objects.all().order_by("-created_at")
    serializer_class = CartSerializer
    lookup_value_regex = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

    def list(self, request):
        cart_list = self.get_queryset()
        for cart in cart_list:
            [
                CartItemService.update_price(item.pk) for item in cart.items.all()
            ] if cart.items else []

            CartService.update_price(cart.pk)
            cart.refresh_from_db()
        self.serializer_class = CartResponseSerializer
        return super().list(request)

    def retrieve(self, request, pk):
        self.serializer_class = CartResponseSerializer
        cart = self.get_object()
        [CartItemService.update_price(item.pk) for item in cart.items.all()]
        CartService.update_price(cart.pk)
        cart.refresh_from_db()
        return super().retrieve(self, request, pk)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.validated_data.get("customer")
        cart, _ = CartService.get_or_create_cart(customer)
        response = CartResponseSerializer(cart)
        return Response(response.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], url_path="items", url_name="clear")
    def clear(self, request, pk=None):
        cart = self.get_object()
        CartService.clear(cart.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
