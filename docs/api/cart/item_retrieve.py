from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from cart.serializers import CartItemSerializer
from docs.api.cart.config import ITEM_EXAMPLE, ITEM_TAGS, NOT_FOUND_SCHEMA

retrieve_schema = extend_schema(
    summary="Get a cart item",
    description="Returns a cart item by its ID.",
    tags=ITEM_TAGS,
    responses={
        200: OpenApiResponse(
            response=CartItemSerializer,
            description="The cart item was found.",
            examples=[
                OpenApiExample(
                    "Item found",
                    summary="Cart item details",
                    value=ITEM_EXAMPLE,
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
