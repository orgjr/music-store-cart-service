from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from cart.serializers import CartSerializer
from docs.api.cart.config import CART_LIST_EXAMPLE, NOT_FOUND_SCHEMA, TAGS

list_schema = extend_schema(
    summary="List carts",
    description="Returns a paginated list of carts.",
    tags=TAGS,
    responses={
        200: OpenApiResponse(
            response=CartSerializer(many=True),
            description="A paginated collection of carts.",
            examples=[
                OpenApiExample(
                    "Cart list",
                    summary="A page of carts",
                    value=CART_LIST_EXAMPLE,
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
