from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from docs.api.cart.config import ITEM_TAGS, NOT_FOUND_SCHEMA

destroy_schema = extend_schema(
    summary="Delete a cart item",
    description="Removes an item from its cart and recalculates the cart total.",
    tags=ITEM_TAGS,
    responses={
        204: OpenApiResponse(description="The item was removed successfully."),
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
