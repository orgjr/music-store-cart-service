from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from cart.serializers import CartSerializer
from docs.api.cart.config import NOT_FOUND_SCHEMA, TAGS

list_schema = extend_schema(
    summary="List carts",
    description="Returns a paginated list of carts.",
    tags=TAGS,
    responses={
        200: CartSerializer(many=True),
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
