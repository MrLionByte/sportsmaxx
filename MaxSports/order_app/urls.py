from django.urls import path
from order_app import views

urlpatterns = [
    path("admin_order/", views.admin_order, name="order_processing"),
    path("order_delivered/", views.admin_delivered, name="order_delivered"),
    path(
        "admin_pending_actions/",
        views.admin_pending_actions,
        name="admin_pending_actions",
    ),
    path("admin_edit_order/", views.admin_edit_order, name="admin_edit_order"),
    path("order_details/<int:order_id>/", views.order_details, name="order_details"),
    path("order_status_change/", views.order_status_change, name="order_status_change"),
    path(
        "order_confirmation/<int:order_id>/",
        views.order_confirmation,
        name="order_confirmation",
    ),
    path(
        "order_cancel_approval/<int:order_id>/",
        views.order_cancel_approval,
        name="order_cancel_approval",
    ),
    path(
        "download_report_in_pdf/",
        views.download_report_in_pdf,
        name="download_report_in_pdf",
    ),
    path("sales_report_excel/", views.sales_report_excel, name="sales_report_excel"),
    # User side
    path("user/order_confirm/", views.order_confirm, name="order_confirm"),
    #     path('user/order_confirm_page/', views.order_confirm_page, name='order_confirm_page'),
    path("user/checkout/add_to_order/", views.add_to_order, name="add_to_order"),
    path("user/user_orders/", views.user_orders, name="user_orders"),
    path(
        "user/user_order_details/<int:order_id>/",
        views.user_order_details,
        name="user_order_details",
    ),
    path("user/cancel_order/<int:order_id>/", views.cancel_order, name="cancel_order"),
    path(
        "order_invoice/<int:serial_number>/", views.order_invoice, name="order_invoice"
    ),
    path(
        "download_invoice/<int:serial_number>/",
        views.download_invoice,
        name="download_invoice",
    ),
]
