from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("/<int:product_id>", views.product),
    path("/add/start", views.add_product),
    path("/add/<int:product_id>", views.add_product_photo),
    path("/<int:product_id>/delete", views.delete_product),
    path("/<int:product_id>/edit/start", views.edit_product),
    path("/<int:product_id>/add_review", views.add_review),
    path("/<int:product_id>/submit_review", views.submit_review),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
