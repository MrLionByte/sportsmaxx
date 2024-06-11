from django.urls import path
from product_app import views

urlpatterns = [
    path("admin_product/", views.admin_product, name="admin_product"),
    path(
        "admin_product_unlisted/",
        views.admin_product_unlisted,
        name="admin_product_unlisted",
    ),
    path("add_product/", views.admin_add_product, name="admin_add_product"),
    path(
        "product/details_product/<int:product_id>/",
        views.admin_details_product,
        name="admin_details_product",
    ),
    path(
        "edit_product/<int:product_id>/",
        views.admin_edit_product,
        name="admin_edit_product",
    ),
    path("feature/<int:product_id>/", views.feature, name="feature"),
    path("unfeature/<int:product_id>/", views.unfeature, name="unfeature"),
    path("edit_variant", views.admin_edit_variant, name="admin_edit_variant"),
    path(
        "edit_product_image/<int:product_id>/",
        views.edit_product_image,
        name="edit_product_image",
    ),
    path(
        "edit_variant/<int:product_id>/",
        views.admin_edit_variant,
        name="admin_edit_variant",
    ),
    path("add_size_qty/", views.admin_add_size_qty, name="admin_add_size_qty"),
    path(
        "admin_edit_size_qty/<int:product_id>/",
        views.admin_edit_size_qty,
        name="admin_edit_size_qty",
    ),
    path(
        "list_product/<int:product_id>/",
        views.admin_list_product,
        name="admin_list_product",
    ),
    path(
        "unlist_product/<int:product_id>/",
        views.admin_unlist_product,
        name="admin_unlist_product",
    ),
    path(
        "productStatus_list/<int:product_id>/",
        views.admin_productStatus_list,
        name="admin_productStatus_list",
    ),
    path(
        "productStatus_unlist/<int:product_id>/",
        views.admin_productStatus_unlist,
        name="admin_productStatus_unlist",
    ),
    path(
        "list_product_type/<int:product_id>/",
        views.product_color_list,
        name="list_product_type",
    ),
    path(
        "unlist_product_type/<int:product_id>/",
        views.product_color_unlist,
        name="unlist_product_type",
    ),
    path(
        "product_color_delete/<int:product_id>/",
        views.product_color_delete,
        name="product_color_delete",
    ),
    path(
        "product_color_undo/<int:product_id>/",
        views.product_color_undo,
        name="product_color_undo",
    ),
    path("user/all_products_list/", views.all_products_list, name="all_products_list"),
    path("user/products/<int:products_id>/", views.user_products, name="user_products"),
    path(
        "user/products/product_details/<int:products_id>/",
        views.product_details,
        name="product_details",
    ),
]
