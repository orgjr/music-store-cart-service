from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from cart.serializers import CartItemSerializer
from docs.api.cart.config import (
    ITEM_EXAMPLE,
    ITEM_TAGS,
    NOT_FOUND_SCHEMA,
    VALIDATION_ERROR_SCHEMA,
)

partial_update_schema = extend_schema(
    summary="Partially update a cart item",
    description=(
        "Updates one or more item fields. For `quantity`, send a positive value "
        "to add units or a negative value to remove units. The item is removed "
        "when its resulting quantity is less than one."
    ),
    tags=ITEM_TAGS,
    request=CartItemSerializer,
    responses={
        200: OpenApiResponse(
            response=CartItemSerializer,
            description="The item was updated successfully.",
            examples=[
                OpenApiExample(
                    "Item updated",
                    summary="Quantity adjusted",
                    value={**ITEM_EXAMPLE, "quantity": 4},
                    response_only=True,
                )
            ],
        ),
        204: OpenApiResponse(
            description="The item was removed because its resulting quantity was less than one."
        ),
        400: OpenApiResponse(
            response=VALIDATION_ERROR_SCHEMA,
            description="The request data is invalid or incomplete.",
            examples=[
                OpenApiExample(
                    "Invalid quantity",
                    summary="Quantity must be an integer",
                    value={"quantity": ["A valid integer is required."]},
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
    examples=[
        OpenApiExample(
            "Quantity adjustment",
            summary="Decrease the quantity by two",
            value={"quantity": -2},
            request_only=True,
        )
    ],
)
