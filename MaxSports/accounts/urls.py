from django.urls import path
from . import views

urlpatterns = [
    path(
        "user_account_details/<int:user_id>/",
        views.user_account_details_admin,
        name="user_account_details_admin",
    ),
    path("my_account/", views.user_profile, name="my_account"),
    path(
        "my_account/add_account_address/",
        views.add_account_address,
        name="add_account_address",
    ),
    path(
        "my_account/delete_address/<int:address_id>/",
        views.delete_address,
        name="delete_address",
    ),
    path(
        "my_account/edit_address/<int:address_id>/",
        views.edit_address,
        name="edit_address",
    ),
    path("my_account/edit_profile/", views.edit_profile, name="edit_profile"),
    path("my_account/change_password/", views.change_password, name="change_password"),
    path(
        "add_checkout_address/", views.add_checkout_address, name="add_checkout_address"
    ),
    path(
        "checkout/edit_checkout_address/<int:address_id>/",
        views.edit_checkout_address,
        name="edit_checkout_address",
    ),
    # path('user/my_account/test/', views.test, name='test'),
]
