from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.basket),
    path("/get", views.get),
    path("/payment", views.payment),
    path("/add/<product_id>", views.add)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
