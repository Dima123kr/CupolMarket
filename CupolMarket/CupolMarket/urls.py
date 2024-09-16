from django.urls import path, include

urlpatterns = [
    path("", include("main.urls")),
    path("account", include("users.urls")),
    path("product", include("products.urls")),
    path("basket", include("basket.urls"))
]
