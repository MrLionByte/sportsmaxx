from django.urls import path
from . import views
from .views import my_custom_404_view
from django.contrib.staticfiles.views import serve


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),  # about page Function
    path("terms/", views.terms, name="terms"),  # terms page Function
    path("contact/", views.contact, name="contact"),
    path("404/", my_custom_404_view, name="handler404"),
]
