from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from core.serializers import HealthResponseSerializer

health_schema = extend_schema(
    summary="Check service health",
    description=(
        "Returns the service status, the current timestamp, and the process uptime "
        "in seconds."
    ),
    tags=["Health"],
    responses={
        200: OpenApiResponse(
            response=HealthResponseSerializer,
            description="The service is healthy and available.",
            examples=[
                OpenApiExample(
                    "Health check OK",
                    summary="Healthy service",
                    value={
                        "status": "ok",
                        "timestamp": "2026-08-03T14:00:00-03:00",
                        "uptime_seconds": 43200,
                    },
                    response_only=True,
                )
            ],
        ),
    },
)
