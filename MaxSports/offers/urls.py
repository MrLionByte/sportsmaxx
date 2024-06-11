from django.urls import path
from offers import views


urlpatterns = [
    path("category_offers", views.category_offers, name="category_offers"),
    path(
        "edit_category_offers/", views.edit_category_offers, name="edit_category_offers"
    ),
    path("product_offers", views.product_offers, name="product_offers"),
    path("edit_product_offers/", views.edit_product_offers, name="edit_product_offers"),
]
