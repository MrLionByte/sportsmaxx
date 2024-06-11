from django.shortcuts import render
from category_app.models import category
from product_app.models import product_color_image
from django.shortcuts import render, redirect
import requests
import time
import psutil
import os
from datetime import datetime
from urllib.parse import urlparse
from django.core.paginator import Paginator
from visitors.models import Visitor
from banner_app.models import main_banner, sub_banner
from django.utils import timezone
from order_app.models import Order_items
from django.db.models import Sum, F, Q
from django.contrib import messages

# Create your views here.
category_data = category.objects.filter(is_listed=True, category_delete=True).order_by(
    "category_name"
)
visitor_count = Visitor.objects.all().count()


# =========   HOME   =========== #
def home(request):
    storage = messages.get_messages(request)
    storage.used = True

    products = product_color_image.objects.all().order_by(
        "product_id__product_updated_at"
    )
    latest_product = product_color_image.objects.filter(
        delete_opt=False,
        status=True,
        product_id__product_delete=False,
        product_id__product_list=True,
    ).order_by("product_id__product_updated_at")[:9]
    trending_product = (
        product_color_image.objects.filter(
            delete_opt=False,
            status=True,
            product_id__product_delete=False,
            product_id__product_list=True,
        )
        .annotate(total_sold=Sum("order_items__quantity"))
        .order_by("total_sold")[:12]
    )
    date_now = timezone.now().date()  # Get the current date
    active_banners = main_banner.objects.filter(
        status=True, start__lte=date_now, expiry__gte=date_now
    )
    context = {
        "category_data": category_data,
        "products": products,
        "trending_product": trending_product,
        "latest_product": latest_product,
        "visitor_count": visitor_count,
        "active_banners": active_banners,
    }
    return render(request, "user/index.html", context)


# =========  END HOME  =========== #


# =========        TERMS       =========== #


def terms(request):
    storage = messages.get_messages(request)
    storage.used = True

    context = {
        "category_data": category_data,
        "visitor_count": visitor_count,
    }
    return render(request, "extra/terms.html", context)


# =========    END TERMS    =========== #

# =========        ABOUT       =========== #


def about(request):
    storage = messages.get_messages(request)
    storage.used = True

    context = {
        "category_data": category_data,
        "visitor_count": visitor_count,
    }
    return render(request, "extra/about.html", context)


# =========    END ABOUT    =========== #

# =========   Contact  =========== #


def contact(request):
    storage = messages.get_messages(request)
    storage.used = True

    context = {
        "category_data": category_data,
        "visitor_count": visitor_count,
    }
    return render(request, "extra/contact.html", context)


# =========    END Contact    =========== #


# =========    404&403 Error    =========== #


def my_custom_404_view(request, exception):
    return render(request, "user/404.html", status=404)


def my_custom_403_view(request, exception):
    return render(request, "404.html", status=404)


# =========    END 404    =========== #
