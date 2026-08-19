from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from cart.serializers import CartResponseSerializer, CartSerializer
from docs.api.cart.config import (
    CART_CREATE_PAYLOAD_EXAMPLE,
    CUSTOMER_CART_EXAMPLE,
    EMPTY_CART_EXAMPLE,
    TAGS,
    VALIDATION_ERROR_SCHEMA,
)

create_schema = extend_schema(
    summary="Create a cart",
    description=(
        "Creates a cart for a customer, or returns the existing one when that "
        "customer already has a cart. If no `customer` is supplied, the shared "
        "anonymous cart is returned. New carts start with a total of zero."
    ),
    tags=TAGS,
    request=CartSerializer,
    responses={
        201: OpenApiResponse(
            response=CartResponseSerializer,
            description="The cart was created or reused successfully.",
            examples=[
                OpenApiExample(
                    "Anonymous cart",
                    summary="Cart created without a customer",
                    value=EMPTY_CART_EXAMPLE,
                    response_only=True,
                ),
                OpenApiExample(
                    "Customer cart",
                    summary="Cart reused for an existing customer",
                    value=CUSTOMER_CART_EXAMPLE,
                    response_only=True,
                ),
            ],
        ),
        400: OpenApiResponse(
            response=VALIDATION_ERROR_SCHEMA,
            description="The request data is invalid.",
            examples=[
                OpenApiExample(
                    "Invalid customer",
                    summary="Customer must be a UUID",
                    value={"customer": ["Must be a valid UUID."]},
                    response_only=True,
                )
            ],
        ),
        500: OpenApiResponse(description="An unexpected server error occurred."),
    },
    examples=[
        OpenApiExample(
            "No customer",
            summary="Create the anonymous cart",
            value={},
            request_only=True,
        ),
        OpenApiExample(
            "With customer",
            summary="Create or reuse a customer's cart",
            value=CART_CREATE_PAYLOAD_EXAMPLE,
            request_only=True,
        ),
    ],
)