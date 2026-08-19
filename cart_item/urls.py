from rest_framework.routers import SimpleRouter

from cart_item.views import CartItemViewSet

router = SimpleRouter()
router.register("", CartItemViewSet, basename="cart-item")

urlpatterns = router.urls
