from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from docs.api.cart.config import NOT_FOUND_SCHEMA, TAGS

clear_schema = extend_schema(
    summary="Clear a cart",
    description="Removes every item from the cart and resets its total to zero.",
    tags=TAGS,
    responses={
        204: OpenApiResponse(description="The cart was cleared successfully."),
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
