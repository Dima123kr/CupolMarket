from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.account),
    path("/register", views.register),
    path("/login", views.login_user),
    path("/logout", views.logout_user),
    path("/edit", views.edit_user),
    path("/delete", views.delete_user),
    path("/admin", views.admin),
    path("/admin/list_of_buyers", views.list_of_buyers),
    path("/admin/list_of_sellers", views.list_of_sellers),
    path("/admin/list_of_admins", views.list_of_admins),
    path("/admin/delete/<int:id>", views.delete_account_for_admin),
    path("/admin/give_admin/<int:id>", views.give_admin),
    path("/admin/give_buyer/<int:id>", views.give_buyer)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
