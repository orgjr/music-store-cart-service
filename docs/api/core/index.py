from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from core.serializers import IndexResponseSerializer

index_schema = extend_schema(
    summary="Get service information",
    description=(
        "Returns service metadata, including its name, version, environment, API "
        "version, and links to the documentation and health endpoints."
    ),
    tags=["Index"],
    responses={
        200: OpenApiResponse(
            response=IndexResponseSerializer,
            description="Service information returned successfully.",
            examples=[
                OpenApiExample(
                    "API index",
                    summary="Service information",
                    value={
                        "name": "Music Store Cart Service",
                        "project_version": "0.9.0",
                        "description": (
                            "An API for managing a music store shopping cart."
                        ),
                        "environment": "development",
                        "redoc_url": "http://localhost:8000/api/v1/redoc/",
                        "health_url": "http://localhost:8000/api/v1/health/",
                        "api_version": "v1",
                    },
                    response_only=True,
                )
            ],
        ),
    },
)
