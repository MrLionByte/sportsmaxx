from django.urls import path
from . import views

urlpatterns = [
    path("user_sign_in/", views.user_sign_in, name="user_sign_in"),
    path("user_sign_up/", views.user_sign_up, name="user_sign_up"),
    path("otp_reg/", views.otp_reg, name="otp_reg"),
    path("email_otp_generator/", views.email_otp_generator, name="email_otp_generator"),
    path("resend_otp/", views.resend_otp, name="resend_otp"),
    path(
        "forgot_password_email/",
        views.forgot_password_email,
        name="forgot_password_email",
    ),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("forgot_password_otp/", views.forgot_password_otp, name="forgot_password_otp"),
    path("user_logout/", views.user_logout, name="user_logout"),
]
