from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from cart.serializers import CartResponseSerializer
from docs.api.cart.config import CART_EXAMPLE, NOT_FOUND_SCHEMA, TAGS

retrieve_schema = extend_schema(
    summary="Get a cart",
    description="Returns a cart and all of its items.",
    tags=TAGS,
    responses={
        200: OpenApiResponse(
            response=CartResponseSerializer,
            description="The cart was found.",
            examples=[
                OpenApiExample(
                    "Cart found",
                    summary="Cart details",
                    value=CART_EXAMPLE,
                    response_only=True,
                )
            ],
        ),
        404: OpenApiResponse(
            response=NOT_FOUND_SCHEMA,
            description="No cart matches the supplied ID.",
            examples=[
                OpenApiExample(
                    "Cart not found",
                    summary="Cart not found",
                    value={"detail": "No Cart matches the given query."},
                    response_only=True,
                )
            ],
        ),
    },
)
