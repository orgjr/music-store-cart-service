from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from cart.serializers import CartItemSerializer
from docs.api.cart.config import (
    ITEM_EXAMPLE,
    ITEM_PAYLOAD_EXAMPLE,
    ITEM_TAGS,
    VALIDATION_ERROR_SCHEMA,
)

create_schema = extend_schema(
    summary="Add an item to a cart",
    description=(
        "Adds a product to a cart. If that product is already in the cart, its "
        "quantity is increased by the requested amount."
    ),
    tags=ITEM_TAGS,
    request=CartItemSerializer,
    responses={
        201: OpenApiResponse(
            response=CartItemSerializer,
            description="The item was added to the cart.",
            examples=[
                OpenApiExample(
                    "Item added",
                    summary="New cart item",
                    value=ITEM_EXAMPLE,
                    response_only=True,
                )
            ],
        ),
        200: OpenApiResponse(
            response=CartItemSerializer,
            description="The item was already in the cart, so its quantity was updated.",
            examples=[
                OpenApiExample(
                    "Item updated",
                    summary="Existing item quantity updated",
                    value={**ITEM_EXAMPLE, "quantity": 3},
                    response_only=True,
                )
            ],
        ),
        400: OpenApiResponse(
            response=VALIDATION_ERROR_SCHEMA,
            description="The request data is invalid or incomplete.",
            examples=[
                OpenApiExample(
                    "Required field missing",
                    summary="Missing product name",
                    value={"product_name": ["This field is required."]},
                    response_only=True,
                ),
                OpenApiExample(
                    "Invalid cart",
                    summary="Unknown cart ID",
                    value={
                        "cart": [
                            (
                                'Invalid pk "00000000-0000-0000-0000-000000000000" - '
                                "object does not exist."
                            )
                        ]
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    "Negative quantity",
                    summary="Quantity cannot be negative",
                    value={"quantity": ["Quantity must be at least 1 when adding an item."]},
                    response_only=True,
                ),
                OpenApiExample(
                    "Zero quantity",
                    summary="Quantity must be at least one",
                    value={"quantity": ["Ensure this value is greater than or equal to 1."]},
                    response_only=True,
                ),
                OpenApiExample(
                    "Negative product id",
                    summary="Invalid product ID",
                    value={"product_id": ["Ensure this value is greater than or equal to 1."]},
                    response_only=True,
                ),
            ],
        ),
        500: OpenApiResponse(description="An unexpected server error occurred."),
    },
    examples=[
        OpenApiExample(
            "New item",
            summary="Add a product to a cart",
            value=ITEM_PAYLOAD_EXAMPLE,
            request_only=True,
        )
    ],
)
