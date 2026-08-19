from django.urls import include, path

urlpatterns = [
    path("", include("core.urls")),
    path("cart/", include("cart.urls")),
    path("cart/items/", include("cart_item.urls")),
]
