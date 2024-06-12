from django.urls import path
from . import views

urlpatterns = [
    path("initiate_payment/", views.initiate_payment, name="initiate_payment"),
    path("payment_failure/",views.payment_failure, name="payment_failure"),
    path(
        "initiate_payment_for_wallet/",
        views.initiate_payment_for_wallet,
        name="initiate_payment_for_wallet",
    ),
]
