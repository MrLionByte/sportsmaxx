from django.urls import path
from coupons_app import views


urlpatterns = [
    path("admin_coupons", views.admin_coupons, name="admin_coupons"),
    path("admin_coupon_add", views.admin_coupon_add, name="admin_coupon_add"),
    path("coupons_expired", views.coupons_expired, name="coupons_expired"),
    path("coupon_list/<int:coupon_id>", views.coupon_list, name="coupon_list"),
    path("coupon_un_list/<int:coupon_id>", views.coupon_un_list, name="coupon_un_list"),
    path("edit_coupon/<int:coupon_id>", views.edit_coupon, name="edit_coupon"),
]
