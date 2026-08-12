from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from cart.serializers import CartItemSerializer
from docs.api.cart.config import (
    ITEM_EXAMPLE,
    ITEM_PAYLOAD_EXAMPLE,
    ITEM_TAGS,
    ITEM_UPDATE_PAYLOAD_EXAMPLE,
    NOT_FOUND_SCHEMA,
    VALIDATION_ERROR_SCHEMA,
)

update_schema = extend_schema(
    summary="Update a cart item",
    description=(
        "Replaces an existing item. `quantity` is the desired final quantity; set "
        "it to `0` to remove the item. All writable item fields are required."
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
                    summary="Item replaced",
                    value={**ITEM_EXAMPLE, "quantity": 3},
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
                    "Required field missing",
                    summary="Required field missing",
                    value={"product_name": ["This field is required."]},
                    response_only=True,
                ),
                OpenApiExample(
                    "Invalid quantity",
                    summary="Quantity must be an integer",
                    value={"quantity": ["A valid integer is required."]},
                    response_only=True,
                ),
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
            "Replace item",
            summary="Replace all writable item fields",
            value=ITEM_UPDATE_PAYLOAD_EXAMPLE,
            request_only=True,
        ),
        OpenApiExample(
            "Remove by quantity",
            summary="Set the quantity to zero",
            value={**ITEM_PAYLOAD_EXAMPLE, "quantity": 0},
            request_only=True,
        ),
    ],
)
