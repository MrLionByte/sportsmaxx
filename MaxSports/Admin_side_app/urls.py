from django.urls import path
from Admin_side_app import views

urlpatterns = [
    path("admin_login/", views.admin_login, name="admin_login"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("next_page/", views.admin_dashboard_page, name="admin_dashboard_page"),
    path(
        "admin_user_management/",
        views.admin_user_management,
        name="admin_user_management",
    ),
    path(
        "admin_user_management_unlisted/",
        views.admin_user_management_unlisted,
        name="admin_user_management_unlisted",
    ),
    path(
        "user_block/<int:user_id>/", views.user_action_block, name="user_action_block"
    ),
    path(
        "user_unblock/<int:user_id>/",
        views.user_action_unblock,
        name="user_action_unblock",
    ),
    path("admin_logout/", views.admin_logout, name="admin_logout"),
]
