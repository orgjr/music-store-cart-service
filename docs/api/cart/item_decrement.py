from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from cart_item.serializers import CartItemResponseSerializer
from docs.api.cart.config import ITEM_EXAMPLE, ITEM_TAGS, NOT_FOUND_SCHEMA

decrement_schema = extend_schema(
    summary="Decrease an item quantity",
    description=(
        "Decreases the item quantity by one and recalculates the cart total. If "
        "the quantity reaches zero, the item is removed from the cart."
    ),
    tags=ITEM_TAGS,
    request=None,
    responses={
        200: OpenApiResponse(
            response=CartItemResponseSerializer,
            description="The item quantity was decreased by one.",
            examples=[
                OpenApiExample(
                    "Item decremented",
                    summary="Quantity decreased by one",
                    value={**ITEM_EXAMPLE, "quantity": 1},
                    response_only=True,
                )
            ],
        ),
        204: OpenApiResponse(
            description="The item was removed because its quantity reached zero."
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
