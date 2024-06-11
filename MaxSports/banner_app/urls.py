from django.urls import path
from . import views

urlpatterns = [
    path("show_banner/", views.show_banner, name="show_banner"),
    path("add_banner/", views.add_banner, name="add_banner"),
    path("edit_banner/", views.edit_banner, name="edit_banner"),
    path("list_banner/", views.list_banner, name="list_banner"),
    path("unlist_banner/", views.unlist_banner, name="unlist_banner"),
]
