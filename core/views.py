from django.conf import settings
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from docs.api.core.health import health_schema
from docs.api.core.index import index_schema

from .helpers.build_url import _build_url
from .helpers.uptime import get_uptime


@index_schema
@api_view(["GET"])
def index(request):
    data = {
        "name": settings.PROJECT_NAME,
        "project_version": settings.PROJECT_VERSION,
        "description": settings.PROJECT_DESCRIPTION,
        "environment": settings.ENVIRONMENT,
        "redoc_url": _build_url("redoc"),
        "health_url": _build_url("health"),
        "api_version": settings.API_ROOT_PREFIX.strip("/").split("/")[-1],
    }
    return Response(data)


@health_schema
@api_view(["GET"])
def health(request):
    data = {
        "status": "ok",
        "timestamp": timezone.localtime().isoformat(),
        "uptime_seconds": get_uptime(),
    }
    return Response(data)
