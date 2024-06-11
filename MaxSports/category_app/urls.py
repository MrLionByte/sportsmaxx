from django.urls import path
from category_app import views

urlpatterns = [
    # Admin Side Category Page
    path("admin_category/", views.admin_category, name="admin_category"),
    path(
        "admin_category_unlisted/",
        views.admin_category_unlisted,
        name="admin_category_unlisted",
    ),
    path("admin_add_category/", views.admin_add_category, name="admin_add_category"),
    path(
        "admin_edit_category/<int:category_id>",
        views.admin_edit_category,
        name="admin_edit_category",
    ),
    path(
        "admin_delete_category/<int:category_id>/",
        views.admin_delete_category,
        name="admin_delete_category",
    ),
    path(
        "admin_undo_category/<int:category_id>/",
        views.admin_undo_category,
        name="admin_undo_category",
    ),
    path(
        "admin_List_category/<int:category_id>/",
        views.admin_List_category,
        name="admin_List_category",
    ),
    path(
        "admin_UnList_category/<int:category_id>/",
        views.admin_UnList_category,
        name="admin_UnList_category",
    ),
    path(
        "admin_types_for_category/",
        views.admin_types_for_category,
        name="admin_types_for_category",
    ),
    path(
        "admin_add_types_for_category/",
        views.admin_add_types_for_category,
        name="admin_add_types_for_category",
    ),
    # User Side Category Page
]
