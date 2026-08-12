from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from cart.serializers import CartItemSerializer
from docs.api.cart.config import ITEM_EXAMPLE, ITEM_TAGS, NOT_FOUND_SCHEMA

increment_schema = extend_schema(
    summary="Increase an item quantity",
    description="Increases the item quantity by one and recalculates the cart total.",
    tags=ITEM_TAGS,
    request=None,
    responses={
        200: OpenApiResponse(
            response=CartItemSerializer,
            description="The item quantity was increased by one.",
            examples=[
                OpenApiExample(
                    "Item incremented",
                    summary="Quantity increased by one",
                    value={**ITEM_EXAMPLE, "quantity": 2},
                    response_only=True,
                )
            ],
        ),
        404: OpenApiResponse(
            response=NOT_FOUND_SCHEMA,
            description="No cart item matches the supplied ID.",
            examples=[
                OpenApiExample(
                    "Item not found",
                    summary="Cart item not found",
                    value={"detail": "No CartItem matches the given query."},
                    response_only=True,
                )
            ],
        ),
    },
)
