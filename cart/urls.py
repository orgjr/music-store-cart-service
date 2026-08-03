from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CartItemViewSet, CartViewSet

router = DefaultRouter()
router.register("", CartViewSet, basename="cart")
router.register("items", CartItemViewSet, basename="cart-item")

urlpatterns = [
    path("", include(router.urls)),
]
