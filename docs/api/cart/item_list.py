from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from cart.serializers import CartItemSerializer
from docs.api.cart.config import ITEM_LIST_EXAMPLE, ITEM_TAGS, NOT_FOUND_SCHEMA

list_schema = extend_schema(
    summary="List cart items",
    description="Returns a paginated list of items from all carts.",
    tags=ITEM_TAGS,
    responses={
        200: OpenApiResponse(
            response=CartItemSerializer(many=True),
            description="A paginated collection of cart items from all carts.",
            examples=[
                OpenApiExample(
                    "Cart item list",
                    summary="A page of cart items",
                    value=ITEM_LIST_EXAMPLE,
                    response_only=True,
                )
            ],
        ),
        404: OpenApiResponse(
            response=NOT_FOUND_SCHEMA,
            description="The requested page does not exist.",
            examples=[
                OpenApiExample(
                    "Invalid page",
                    summary="Page not found",
                    value={"detail": "Invalid page."},
                    response_only=True,
                )
            ],
        ),
        500: OpenApiResponse(description="An unexpected server error occurred."),
    },
)
