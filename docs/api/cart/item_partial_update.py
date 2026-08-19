from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from cart_item.serializers import CartItemResponseSerializer, CartItemSerializer
from docs.api.cart.config import (
    ITEM_EXAMPLE,
    ITEM_TAGS,
    NOT_FOUND_SCHEMA,
    VALIDATION_ERROR_SCHEMA,
)

partial_update_schema = extend_schema(
    summary="Partially update a cart item",
    description=(
        "Updates one or more item fields. When supplied, `quantity` replaces the "
        "current quantity; a value of `0` removes the item."
    ),
    tags=ITEM_TAGS,
    request=CartItemSerializer,
    responses={
        200: OpenApiResponse(
            response=CartItemResponseSerializer,
            description="The item was updated successfully.",
            examples=[
                OpenApiExample(
                    "Item updated",
                    summary="Quantity replaced",
                    value={**ITEM_EXAMPLE, "quantity": 3, "price": "3750.00"},
                    response_only=True,
                )
            ],
        ),
        204: OpenApiResponse(
            description="The item was removed because its quantity was set to zero."
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
            "Set quantity",
            summary="Set the item quantity to three",
            value={"quantity": 3},
            request_only=True,
        )
    ],
)
