from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import PwdResetConfirmForm, PwdResetForm, UserLoginForm

# https://docs.djangoproject.com/en/3.1/topics/auth/default/
# https://ccbv.co.uk/projects/Django/3.0/django.contrib.auth.views/PasswordResetConfirmView/

app_name = "account"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="account/login.html", form_class=UserLoginForm),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/account/login/"), name="logout"),
    path("register/", views.account_register, name="register"),
    path("activate/<slug:uidb64>/<slug:token>)/", views.account_activate, name="activate"),
    # Reset password
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password_reset/password_reset_form.html",
            success_url="password_reset_email_confirm",
            email_template_name="account/password_reset/password_reset_email.html",
            form_class=PwdResetForm,
        ),
        name="pwdreset",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password_reset/password_reset_confirm.html",
            success_url="password_reset_complete/",
            form_class=PwdResetConfirmForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/password_reset_email_confirm/",
        TemplateView.as_view(template_name="account/password_reset/reset_status.html"),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/password_reset_complete/",
        TemplateView.as_view(template_name="account/password_reset/reset_status.html"),
        name="password_reset_complete",
    ),
    # User dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/edit/", views.edit_details, name="edit_details"),
    path("profile/delete_user/", views.delete_user, name="delete_user"),
    path(
        "profile/delete_confirm/",
        TemplateView.as_view(template_name="account/dashboard/delete_confirm.html"),
        name="delete_confirmation",
    ),
    path("addresses/", views.view_address, name="addresses"),
    path("add_address/", views.add_address, name="add_address"),
    path("add_address_tmp/", views.add_address_tmp, name="add_address_tmp"),
    path("addresses/edit/<slug:id>/", views.edit_address, name="edit_address"),
    path("addresses/delete/<slug:id>/", views.delete_address, name="delete_address"),
    path("addresses/set_default/<slug:id>/", views.set_default, name="set_default"),
    path("user_orders/", views.user_orders, name="user_orders"),
    # Wish List
    path("wishlist", views.wishlist, name="wishlist"),
    path("wishlist/add_to_wishlist/<int:id>", views.add_to_wishlist, name="user_wishlist"),
    path("wishlist/remove_from_wishlist/<int:id>", views.remove_from_wishlist, name="remove_wishlist"),
    # Product management
    path("product_manage", views.user_product_manage, name="product_manage"),
    path("add", views.ProductAdd, name="Product_add"),
    path("update/<int:pid>", views.ProductUpdate, name="Product_update"),
    path("delete/<int:pk>", views.ProductDelete.as_view(), name="Product_delete"),
    path("item_order/<int:pid>", views.ItemOrder, name="item_order"),
    path("all_order/", views.AllOrder, name="All_order"),
    path('finish_confirm/<int:order_id>', views.finish_confirm, name='finish_confirm'),
    path('view_seller/<slug:seller_id>', views.view_seller, name="view_seller")
]
