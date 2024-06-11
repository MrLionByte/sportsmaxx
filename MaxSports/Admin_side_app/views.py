from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from category_app.models import category
from order_app.models import Order, Order_items
from datetime import datetime
from django.utils import timezone
from datetime import timedelta, date
import calendar
from django.utils import timezone as django_timezone
from django.db.models import Sum
from openpyxl import Workbook
from openpyxl.styles import *
import decimal
import datetime as datetime_all
from visitors.models import Visitor
from category_app.models import category

from django.db.models import Count, Func
from django.db.models.functions import TruncYear, TruncMonth, TruncDay
from django.utils.timezone import make_aware
from datetime import datetime

from . import graph

# Create your views here.


"""
Render admin login page and only allow admin to log in
"""


@never_cache
def admin_login(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == "POST":
        admin_name = request.POST.get("username")
        admin_password = request.POST.get("password")
        admin_object = authenticate(
            request, username=admin_name, password=admin_password
        )
        if admin_object is not None:
            login(request, admin_object)
            return redirect("admin_dashboard")
        messages.error(request, "invalid password or username")
    return render(request, "admin/admin_login.html")


"""
Render admin_dashboard page and only allow admin to enter into the page
"""


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_dashboard(request):
    storage = messages.get_messages(request)
    storage.used = True

    sort_id = request.GET.get("sort_id")

    sales_report = Order_items.objects.filter(status="Delivered").order_by(
        "-last_update"
    )
    request.session["type_report"] = None
    if request.method == "POST":
        start_date = request.POST.get("starting")
        end_date = request.POST.get("ending")
        if not end_date:
            sales_report = Order_items.objects.filter(
                status="Delivered", order__order_date__gte=start_date
            ).order_by("-last_update")
            request.session["start_date"] = str(start_date)
            request.session["type_report"] = "start_date"
        elif not start_date:
            sales_report = Order_items.objects.filter(
                status="Delivered", order__order_date__lte=end_date
            ).order_by("-last_update")
            request.session["end_date"] = str(end_date)
            request.session["type_report"] = "end_date"
        elif start_date and end_date:
            sales_report = Order_items.objects.filter(
                status="Delivered",
                order__order_date__gte=start_date,
                order__order_date__lte=end_date,
            ).order_by("-last_update")
            request.session["end_date"] = str(end_date)
            request.session["start_date"] = str(start_date)
            request.session["type_report"] = "total_date"
    if sort_id is not None:
        if sort_id == "now":
            now = datetime.today().date()
            sales_report = Order_items.objects.filter(
                status="Delivered", order__order_date__lte=now
            ).order_by("-last_update")

            request.session["now"] = str(now)
            request.session["type_report"] = "now"
        elif sort_id == "week":
            start_of_week = timezone.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            if timezone.now().weekday() == 0:
                start_of_week -= timedelta(days=7)

            end_of_week = start_of_week + timedelta(days=6)

            sales_report = Order_items.objects.filter(
                status="Delivered",
                order__order_date__gte=start_of_week,
                order__order_date__lte=end_of_week,
            ).order_by("-last_update")
            request.session["start_of_week"] = str(start_of_week)
            request.session["end_of_week"] = str(end_of_week)
            request.session["type_report"] = "week"
        elif sort_id == "month":
            this_month = date.today().month
            sales_report = Order_items.objects.filter(
                status="Delivered", order__order_date__month=(this_month)
            ).order_by("-last_update")
            request.session["this_month"] = str(this_month)

            request.session["type_report"] = "month"
        elif sort_id == "year":
            year = date.today().year
            sales_report = Order_items.objects.filter(
                status="Delivered", order__order_date__year=year
            ).order_by("-last_update")
            request.session["year"] = str(year)

            request.session["type_report"] = "year"

    if sales_report:
        over_all_price = sales_report.aggregate(total_amount=Sum("order__total_amount"))
        over_all_price = over_all_price["total_amount"]
        over_all_discount_price = sales_report.aggregate(
            total_product_price=Sum("final_product_price")
        )
        over_all_discount_price = over_all_discount_price["total_product_price"]
        over_all_discount_price = over_all_price - over_all_discount_price
        over_all_sales = sales_report.count()
    else:
        over_all_sales = None
        over_all_price = None
        over_all_discount_price = None

    order_items_filtered = graph.order_items_count()
    aggregation_type = request.GET.get("type")
    if aggregation_type is None:
        aggregation_type = "yearly"
    sales_report_graph_main = graph.sales_report_graph_main(aggregation_type)

    category_per_products_sold = graph.category_per_products_sold()
    category_names = category_per_products_sold[0]
    total_sold_values = category_per_products_sold[1]

    product_per_products_sold = graph.product_per_products_sold()
    top_product_names = product_per_products_sold[0]
    top_product_sold_values = product_per_products_sold[1]

    variants_of_products_sold = graph.variants_of_products_sold()
    top_variants_names = variants_of_products_sold[0]
    top_variants_sold_values = variants_of_products_sold[1]

    top_selling_products = dict(zip(top_product_names[:4], top_product_sold_values[:4]))
    top_selling_category = dict(zip(category_names, total_sold_values))
    top_selling_variants = dict(zip(top_variants_names, top_variants_sold_values))
    top_selling_variants_sorted = dict(
        sorted(top_selling_variants.items(), key=lambda item: item[1], reverse=True)
    )

    page_check = request.session.get("page_check")
    print(page_check)
    context = {
        "page_check": page_check,
        "sales_report": sales_report,
        "over_all_sales": over_all_sales,
        "over_all_price": over_all_price,
        "over_all_discount": over_all_discount_price,
        "orders_completed": Order_items.objects.filter(status="Delivered").count(),
        "no_of_orders": Order_items.objects.all().count(),
        "visitor_count": Visitor.objects.all().count(),
        "Visitor_percentage": Visitor.today_vs_month_percentage(),
        "sales_today": graph.todays_sale(),
        "year_of_sale": sales_report_graph_main["sales_report_type"],
        "sales_report_delivered": sales_report_graph_main["sales_report_delivered"],
        "sales_report_cancelled": sales_report_graph_main["sales_report_cancelled"],
        "sales_report_returned": sales_report_graph_main["sales_report_returned"],
        "order_items_filtered": order_items_filtered,
        "category_names": category_names,
        "total_sold_values": total_sold_values,
        "top_product_names": top_product_names,
        "top_product_sold_values": top_product_sold_values,
        "top_selling_products": top_selling_products,
        "top_selling_category": top_selling_category,
        "top_selling_variants": top_selling_variants_sorted,
    }
    return render(request, "admin/admin_dashboard.html", context)


def admin_dashboard_page(request):
    page_next = request.GET.get("page_next")
    print(page_next)
    request.session["page_check"] = page_next
    return redirect("admin_dashboard")


"""
Render admin_ user_management page and show all unblocked users
"""


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_user_management(request):
    storage = messages.get_messages(request)
    storage.used = True

    search_query = request.POST.get("search", "")
    if search_query:
        customer_data = User.objects.filter(
            Q(username__icontains=search_query, is_active=True)
            | Q(email__icontains=search_query, is_active=True)
        )
    else:
        customer_data = User.objects.filter(is_active=True).order_by("id", "username")
    context = {"customer_data": customer_data}
    return render(request, "admin/admin_user_management.html", context)


"""
Render admin_ user_management page and show all blocked users
"""


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_user_management_unlisted(request):
    storage = messages.get_messages(request)
    storage.used = True

    search_query = request.POST.get("search", "")
    if search_query:
        customer_data = User.objects.filter(
            Q(username__icontains=search_query, is_active=False)
            | Q(email__icontains=search_query, is_active=False)
        )
    else:
        customer_data = User.objects.filter(is_active=False).order_by("id", "username")
    context = {"customer_data": customer_data}
    return render(request, "admin/admin_user_management_blocked.html", context)


"""
Allow  admin to show all blocked users
"""


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def user_action_unblock(request, user_id):
    storage = messages.get_messages(request)
    storage.used = True

    action_on_user = User.objects.get(id=user_id)
    action_on_user.is_active = False
    action_on_user.save()
    return redirect("admin_user_management")


"""
Allow  admin to show all blocked users
"""


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def user_action_block(request, user_id):
    storage = messages.get_messages(request)
    storage.used = True

    action_on_user = User.objects.get(id=user_id)
    action_on_user.is_active = True
    action_on_user.save()
    return redirect("admin_user_management")


# ========  END User_management Action ======== #


# ========  Admin Logout ======== #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_logout(request):
    if request.user.is_superuser:
        logout(request)
        return redirect("admin_login")
    return redirect("admin_login")


# ========  END Logout ======== #
