from django.urls import path
from . import views

urlpatterns = [
    path("user/cart/", views.cart_show, name="cart_show"),
    path(
        "user/add_product_to_cart/",
        views.add_product_to_cart,
        name="add_product_to_cart",
    ),
    path("cart/remove_from_cart/", views.remove_from_cart, name="remove_from_cart"),
    path("update_total_price/", views.update_total_price, name="update_total_price"),
    path("apply_coupon/", views.apply_coupon, name="apply_coupon"),
    path("delete_coupon/", views.delete_coupon, name="delete_coupon"),
    path(
        "user/cart/checkout_product/", views.checkout_product, name="checkout_product"
    ),
    path("user/cart/show_wishlist/", views.show_wishlist, name="show_wishlist"),
    path(
        "user/cart/add_to_wishlist/<int:product_id>/",
        views.add_to_wishlist,
        name="add_to_wishlist",
    ),
    path(
        "user/cart/delete_from_wishlist/",
        views.delete_from_wishlist,
        name="delete_from_wishlist",
    ),
]
