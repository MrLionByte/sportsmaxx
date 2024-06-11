from order_app.models import Order_items
from django.db.models import Count, Func
from django.db.models.functions import TruncYear, TruncMonth, TruncDay
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.db.models import Sum

from django.db.models import Count, Func
from django.db.models.functions import TruncYear, TruncMonth, TruncDay
from django.utils.timezone import make_aware
from django.utils import timezone
from datetime import datetime

"""
Here written functions for getting data to chart or graph nin dashboard
"""


def order_items_count():
    order_items_filtered = [
        Order_items.objects.filter(status="Order confirmed").count(),
        Order_items.objects.filter(status="Shipped").count(),
        Order_items.objects.filter(status="Out For Delivery").count(),
        Order_items.objects.filter(status="Delivered").count(),
        Order_items.objects.filter(status="Cancelled").count(),
        Order_items.objects.filter(status="Returned").count(),
    ]
    return order_items_filtered


def category_per_products_sold():
    category_names = []
    total_sold_values = []
    products_sold = (
        Order_items.objects.filter(status="Delivered")
        .values("product_added__product_id__category_id__category_name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-product_added__product_id__category_id__category_name")
    )
    for entry in products_sold:
        category_names.append(
            entry["product_added__product_id__category_id__category_name"]
        )
        total_sold_values.append(entry["total_sold"])

    return [category_names, total_sold_values]


def product_per_products_sold():
    top_product_names = []
    top_product_sold_values = []
    top_products_sold = (
        Order_items.objects.filter(status="Delivered")
        .values("product_added__product_id__product_name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:10]
    )
    for entry in top_products_sold:
        top_product_names.append(entry["product_added__product_id__product_name"])
        top_product_sold_values.append(entry["total_sold"])

    return [top_product_names, top_product_sold_values]


def variants_of_products_sold():
    variant_names = []
    total_variant_values = []
    variants_sold = (
        Order_items.objects.filter(status="Delivered")
        .values("product_added__product_variant_name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-product_added__product_variant_name")
    )
    for entry in variants_sold:
        variant_names.append(entry["product_added__product_variant_name"])
        total_variant_values.append(entry["total_sold"])

    return [variant_names, total_variant_values]


def sales_report_graph_main(aggregation_type):
    if aggregation_type == "yearly":
        start_date_str = "2022-01-01"
        end_date_str = "2028-12-31"
    elif aggregation_type == "monthly":
        current_date = timezone.now().date()
        start_date_str = f"{current_date.year}-01-01"
        end_date_str = f"{current_date.year}-12-01"
    elif aggregation_type == "daily":
        current_date = timezone.now().date()
        start_date_str = f"{current_date.year}-{current_date.month}-01"
        end_date_str = f"{current_date.year}-{current_date.month}-30"

    try:
        start_date = make_aware(datetime.strptime(start_date_str, "%Y-%m-%d"))
        end_date = make_aware(datetime.strptime(end_date_str, "%Y-%m-%d"))
    except ValueError:
        start_date = make_aware(datetime.strptime(start_date_str, "%Y-%m-%d"))
        end_date_str = end_date_str[:-2] + "30"
        end_date = make_aware(datetime.strptime(end_date_str, "%Y-%m-%d"))

    if aggregation_type == "yearly":
        trunc_func = TruncYear
        date_format = "%Y"
    elif aggregation_type == "monthly":
        trunc_func = TruncMonth
        date_format = "%Y-%m"
    elif aggregation_type == "daily":
        trunc_func = TruncDay
        date_format = "%Y-%m-%d"

    order_items_delivered_count = (
        Order_items.objects.filter(
            status="Delivered", order__order_date__range=(start_date, end_date)
        )
        .annotate(period=trunc_func("order__order_date"))
        .values("period")
        .annotate(count=Count("id"))
        .values("period", "count")
    )

    counts = {}
    for item in order_items_delivered_count:
        period = item["period"].strftime(date_format)
        counts[period] = item["count"]

    current_date = start_date
    while current_date <= end_date:
        period = current_date.strftime(date_format)
        if period not in counts:
            counts[period] = 0
        if aggregation_type == "yearly":
            current_date = current_date.replace(
                year=current_date.year + 1, month=1, day=1
            )
        elif aggregation_type == "monthly":
            if current_date.month == 12:
                current_date = current_date.replace(
                    year=current_date.year + 1, month=1, day=1
                )
            else:
                current_date = current_date.replace(month=current_date.month + 1, day=1)
        elif aggregation_type == "daily":
            current_date += timedelta(days=1)

    order_items_delivered_count = (
        Order_items.objects.filter(
            status="Delivered", order__order_date__range=(start_date, end_date)
        )
        .annotate(period=trunc_func("order__order_date"))
        .values("period")
        .annotate(count=Count("id"))
        .values("period", "count")
    )

    counts_delivered = {}
    for item in order_items_delivered_count:
        period = item["period"].strftime(date_format)
        counts_delivered[period] = item["count"]

    current_date = start_date
    while current_date <= end_date:
        period = current_date.strftime(date_format)
        if period not in counts_delivered:
            counts_delivered[period] = 0
        if aggregation_type == "yearly":
            current_date = current_date.replace(
                year=current_date.year + 1, month=1, day=1
            )
        elif aggregation_type == "monthly":
            if current_date.month == 12:
                current_date = current_date.replace(
                    year=current_date.year + 1, month=1, day=1
                )
            else:
                current_date = current_date.replace(month=current_date.month + 1, day=1)
        elif aggregation_type == "daily":
            current_date += timedelta(days=1)

    order_items_cancelled_count = (
        Order_items.objects.filter(
            status="Cancelled", order__order_date__range=(start_date, end_date)
        )
        .annotate(period=trunc_func("order__order_date"))
        .values("period")
        .annotate(count=Count("id"))
        .values("period", "count")
    )

    counts_cancelled = {}
    for item in order_items_cancelled_count:
        period = item["period"].strftime(date_format)
        counts_cancelled[period] = item["count"]

    current_date = start_date
    while current_date <= end_date:
        period = current_date.strftime(date_format)
        if period not in counts_cancelled:
            counts_cancelled[period] = 0
        if aggregation_type == "yearly":
            current_date = current_date.replace(
                year=current_date.year + 1, month=1, day=1
            )
        elif aggregation_type == "monthly":
            if current_date.month == 12:
                current_date = current_date.replace(
                    year=current_date.year + 1, month=1, day=1
                )
            else:
                current_date = current_date.replace(month=current_date.month + 1, day=1)
        elif aggregation_type == "daily":
            current_date += timedelta(days=1)

    order_items_returned_count = (
        Order_items.objects.filter(
            status="Returned", order__order_date__range=(start_date, end_date)
        )
        .annotate(period=trunc_func("order__order_date"))
        .values("period")
        .annotate(count=Count("id"))
        .values("period", "count")
    )

    counts_returned = {}
    for item in order_items_returned_count:
        period = item["period"].strftime(date_format)
        counts_returned[period] = item["count"]

    current_date = start_date
    while current_date <= end_date:
        period = current_date.strftime(date_format)
        if period not in counts_returned:
            counts_returned[period] = 0
        if aggregation_type == "yearly":
            current_date = current_date.replace(
                year=current_date.year + 1, month=1, day=1
            )
        elif aggregation_type == "monthly":
            if current_date.month == 12:
                current_date = current_date.replace(
                    year=current_date.year + 1, month=1, day=1
                )
            else:
                current_date = current_date.replace(month=current_date.month + 1, day=1)
        elif aggregation_type == "daily":
            current_date += timedelta(days=1)

    data = {
        "sales_report_type": list(sorted(counts_delivered.keys())),
        "sales_report_delivered": [
            counts_delivered[period] for period in sorted(counts_delivered.keys())
        ],
        "sales_report_cancelled": [
            counts_cancelled[period] for period in sorted(counts_cancelled.keys())
        ],
        "sales_report_returned": [
            counts_returned[period] for period in sorted(counts_returned.keys())
        ],
    }
    return data


def todays_sale():
    start_of_today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_today = start_of_today + timedelta(days=1)
    sales_today = Order_items.objects.filter(
        status="Delivered",
        last_update__gte=start_of_today,
        last_update__lt=end_of_today,
    ).count()
    return sales_today
