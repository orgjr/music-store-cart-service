from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from cart.serializers import CartSerializer
from docs.api.cart.config import CART_EXAMPLE, TAGS

create_schema = extend_schema(
    summary="Create a cart",
    description="Creates a new empty cart with a total of zero.",
    tags=TAGS,
    responses={
        201: OpenApiResponse(
            response=CartSerializer,
            description="The cart was created successfully.",
            examples=[
                OpenApiExample(
                    "Cart created",
                    summary="New cart",
                    value=CART_EXAMPLE,
                    response_only=True,
                )
            ],
        ),
        500: OpenApiResponse(description="An unexpected server error occurred."),
    },
)
