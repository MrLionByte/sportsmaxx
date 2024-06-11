from django.urls import path
from . import views

urlpatterns = [
    path("user/wallet/", views.user_wallet, name="user_wallet"),
    path(
        "user/wallet/update_wallet_balance/",
        views.update_wallet_balance,
        name="update_wallet_balance",
    ),
]
