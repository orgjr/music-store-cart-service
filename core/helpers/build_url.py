from django.conf import settings


def _build_url(path: str) -> str:
    urls = {
        "redoc": f"{settings.API_ROOT_PREFIX}redoc/",
        "health": f"{settings.API_ROOT_PREFIX}health/",
    }
    return urls.get(path, "")
