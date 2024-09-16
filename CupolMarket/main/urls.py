from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.main),
    path("load_more", views.load_more),
    path("load_more_search", views.load_more_search),
    path("get_seller_products", views.get_seller_products),
    path("about_us", views.about_us),
    path("subscribe", views.subscribe),
    path("search/<query>", views.search_result),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
