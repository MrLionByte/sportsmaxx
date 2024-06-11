from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Order, user_address, Order_items
from cart_app.models import Cart, Checkout, Cart_products
from django.core.exceptions import ValidationError
from django.utils import timezone
from product_app.models import product_sizes_variants
from payment import views
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Sum, aggregates
from wallet.models import Wallet_transactions, Wallet_User
from django.views.decorators.cache import never_cache
from decimal import Decimal

from django.http import FileResponse
from io import BytesIO
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from datetime import datetime
from reportlab.lib import colors
from django.template.loader import get_template
from django.http import HttpResponse
from .pdf import html_to_pdf, HttpResponse

import xlsxwriter
from django.utils import timezone
import datetime as datetime_all

from django.template import loader
import weasyprint

from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.db.models import Sum, Count

# from django.db.models.functions import TruncDate


# Create your views here.


"""
Download sales report in PDF and EXCEL
"""


# ============  SALES REPORT IN PDF ===============#
@never_cache
@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def download_report_in_pdf(request):
    storage = messages.get_messages(request)
    storage.used = True

    sales_report = Order_items.objects.filter(status="Delivered").order_by(
        "-last_update"
    )
    if request.session.get("type_report") == "now":
        now = request.session.get("now")
        now = datetime.strptime(now, "%Y-%m-%d")
        sales_report = Order_items.objects.filter(
            status="Delivered", order__order_date__lte=now
        ).order_by("-last_update")
    elif request.session.get("type_report") == "week":
        start_of_week = request.session.get("start_of_week")
        end_of_week = request.session.get("end_of_week")
        sales_report = Order_items.objects.filter(
            status="Delivered",
            order__order_date__gte=start_of_week,
            order__order_date__lte=end_of_week,
        ).order_by("-last_update")
    elif request.session.get("type_report") == "month":
        this_month = request.session.get("this_month")
        sales_report = Order_items.objects.filter(
            status="Delivered", order__order_date__month=this_month
        ).order_by("-last_update")
    elif request.session.get("type_report") == "year":
        year = request.session.get("year")
        sales_report = Order_items.objects.filter(
            status="Delivered", order__order_date__year=year
        ).order_by("-last_update")
    elif request.session.get("type_report") == "start_date":
        start_date = request.session.get("start_date")
        sales_report = Order_items.objects.filter(
            status="Delivered", order__order_date__gte=start_date
        ).order_by("-last_update")
    elif request.session.get("type_report") == "end_date":
        end_date = request.session.get("end_date")
        sales_report = Order_items.objects.filter(
            status="Delivered", order__order_date__lte=end_date
        ).order_by("-last_update")
    elif request.session.get("type_report") == "total_date":
        start_date = request.session.get("start_date")
        end_date = request.session.get("end_date")
        sales_report = Order_items.objects.filter(
            status="Delivered",
            order__order_date__gte=start_date,
            order__order_date__lte=end_date,
        ).order_by("-last_update")

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()
    centered_style = ParagraphStyle(
        name="Centered", parent=styles["Heading1"], alignment=1
    )

    today_date = datetime.now().strftime("%Y-%m-%d")

    content = []

    company_details = (
        f"<b>SPORTSMAXX</b><br/>Email: sportsmaxx@gmail.com<br/>Date: {today_date}"
    )
    content.append(Paragraph(company_details, styles["Normal"]))
    content.append(Spacer(1, 0.5 * inch))

    content.append(Paragraph("<b>SALES REPORT</b><hr>", centered_style))
    content.append(Spacer(1, 0.5 * inch))

    data = [["Order ID", "Product", "Quantity", "Total Price", "Date"]]
    for sale in sales_report:
        formatted_date = sale.order.order_date.strftime("%a, %d %b %Y")
        data.append(
            [
                sale.order.serial_number,
                sale.product_added.product_id.product_name
                + "("
                + sale.product_added.product_color
                + ")",
                sale.quantity,
                sale.final_product_price,
                formatted_date,
            ]
        )

    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("TOPPADDING", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    overall_sales_count = Order_items.objects.filter(status="Delivered").count()
    overall_order_amount = Order_items.objects.filter(status="Delivered").aggregate(
        total_sales=Sum("final_product_price")
    )["total_sales"]
    overall_order_discount = Order_items.objects.filter(status="Delivered").aggregate(
        total_sales=Sum("order__total_amount")
    )["total_sales"]
    Total_sales_count = sales_report.count()
    Total_sales_price = sales_report.aggregate(
        total_product_price=Sum("final_product_price")
    )["total_product_price"]
    content.append(table)
    content.append(Spacer(1, 0.5 * inch))

    Total_sales_count_text = f"<b>Total sales count:</b> {Total_sales_count}"
    Total_sales_price_text = f"<b>Total sales price:</b> {Total_sales_price}"

    overall_order_discount = overall_order_amount - overall_order_discount

    overall_sales_count_text = f"<b>Overall Sales Count:</b> {overall_sales_count}"
    overall_order_amount_text = f"<b>Overall Order Amount:</b> {overall_order_amount}"
    overall_order_discount_text = (
        f"<b>Overall Order Discount:</b> {overall_order_discount}"
    )

    content.append(Paragraph(Total_sales_count_text, styles["Normal"]))
    content.append(Paragraph(Total_sales_price_text, styles["Normal"]))

    content.append(Spacer(1, 0.2 * inch))
    content.append(Spacer(1, 0.2 * inch))

    content.append(Paragraph(overall_sales_count_text, styles["Normal"]))
    content.append(Paragraph(overall_order_amount_text, styles["Normal"]))
    content.append(Paragraph(overall_order_discount_text, styles["Normal"]))

    doc.build(content)

    current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    file_name = f"Sales_Report_{current_time}.pdf"

    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{file_name}"'

    return response


# ============ END SALES REPORT IN pdf ===============#


# ============ SALES REPORT IN Excel ===============#
@never_cache
@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def sales_report_excel(request):
    storage = messages.get_messages(request)
    storage.used = True

    sales_report = Order_items.objects.filter(status="Delivered").order_by(
        "-last_update"
    )
    if request.session.get("type_report") == "now":
        now = request.session.get("now")
        now = datetime_all.datetime.strptime(now, "%Y-%m-%d")
        sales_report = Order_items.objects.filter(
            status="Delivered", order__order_date__lte=now
        ).order_by("-last_update")
    if request.session.get("type_report") == "week":
        start_of_week = request.session.get("start_of_week")
        end_of_week = request.session.get("end_of_week")
        sales_report = Order_items.objects.filter(
            status="Delivered",
            order__order_date__gte=start_of_week,
            order__order_date__lte=end_of_week,
        ).order_by("-last_update")
    if request.session.get("type_report") == "month":
        this_month = request.session.get("this_month")
        sales_report = Order_items.objects.filter(
            status="Delivered", order__order_date__month=(this_month)
        ).order_by("-last_update")
    if request.session.get("type_report") == "year":
        year = request.session.get("year")
        sales_report = Order_items.objects.filter(
            status="Delivered", order__order_date__year=year
        ).order_by("-last_update")
    if request.session.get("type_report") == "start_date":
        start_date = request.session.get("start_date")
        sales_report = Order_items.objects.filter(
            status="Delivered", order__order_date__gte=start_date
        ).order_by("-last_update")
    if request.session.get("type_report") == "end_date":
        end_date = request.session.get("end_date")
        sales_report = Order_items.objects.filter(
            status="Delivered", order__order_date__lte=end_date
        ).order_by("-last_update")
    if request.session.get("type_report") == "total_date":
        start_date = request.session.get("start_date")
        end_date = request.session.get("end_date")
        sales_report = Order_items.objects.filter(
            status="Delivered",
            order__order_date__gte=start_date,
            order__order_date__lte=end_date,
        ).order_by("-last_update")

    overall_sales_count = Order_items.objects.filter(status="Delivered").count()
    overall_order_amount = Order_items.objects.filter(status="Delivered").aggregate(
        total_sales=Sum("final_product_price")
    )["total_sales"]
    overall_order_discount = Order_items.objects.filter(status="Delivered").aggregate(
        total_sales=Sum("order__total_amount")
    )["total_sales"]
    Total_sales_count = sales_report.count()
    Total_sales_price = sales_report.aggregate(
        total_product_price=Sum("final_product_price")
    )["total_product_price"]

    Total_sales_count_text = f"Total sales count: {Total_sales_count}"
    Total_sales_price_text = f"Total sales price: {Total_sales_price}"
    overall_order_discount = overall_order_amount - overall_order_discount
    overall_sales_count_text = f"Overall Sales Count: {overall_sales_count}"
    overall_order_amount_text = f"Overall Order Amount: {overall_order_amount}"
    overall_order_discount_text = f"Overall Order Discount: {
        overall_order_discount}"

    output = BytesIO()

    workbook = xlsxwriter.Workbook(output, {"in_memory": True})
    worksheet = workbook.add_worksheet("Sales Report")

    merge_format = workbook.add_format(
        {"bold": True, "align": "center", "valign": "vcenter", "font_size": 14}
    )

    worksheet.merge_range("A1:F1", "SportsMaxx", merge_format)
    worksheet.merge_range("A2:F2", "SALES Report", merge_format)

    headings = ["Order ID", "Product", "Customer", "Quantity", "Total Price", "Date"]
    header_format = workbook.add_format({"bold": True})
    for col, heading in enumerate(headings):
        worksheet.write(2, col, heading, header_format)

    for row, sale in enumerate(sales_report, start=3):
        formatted_date = sale.order.order_date.strftime("%a, %d %b %Y")
        worksheet.write(row, 0, sale.order.serial_number)
        worksheet.write(row, 1, sale.product_added.product_id.product_name)
        worksheet.write(row, 2, sale.order.user_id.username)
        worksheet.write(row, 3, sale.quantity)
        worksheet.write(row, 4, sale.final_product_price)
        worksheet.write(row, 5, formatted_date)

    summary_start_row = row + 2
    worksheet.write(summary_start_row, 0, Total_sales_count_text)
    worksheet.write(summary_start_row + 1, 0, Total_sales_price_text)
    worksheet.write(summary_start_row + 2, 0, overall_sales_count_text)
    worksheet.write(summary_start_row + 3, 0, overall_order_amount_text)
    worksheet.write(summary_start_row + 4, 0, overall_order_discount_text)

    workbook.close()
    output.seek(0)
    response = HttpResponse(
        output.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    file_name = f"Sales_Report_{current_time}.xlsx"
    response["Content-Disposition"] = f'attachment; filename="{file_name}"'

    return response


# ============ END SALES REPORT IN Excel ===============#


"""
Render admin_order page and show all order data of Customers by from Admin side 
"""


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_order(request):
    storage = messages.get_messages(request)
    storage.used = True

    orders = Order_items.objects.all().order_by("-last_update")
    context = {
        "orders": orders,
    }
    return render(request, "admin/admin_order.html", context)


"""
Render oder_delivered page and show all order data of Customers by from Admin.
"""


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_delivered(request):
    storage = messages.get_messages(request)
    storage.used = True

    orders = Order_items.objects.filter(status="Delivered")
    context = {
        "orders": orders,
    }
    return render(request, "admin/admin_order_delivered.html", context)


"""
Render oder_delivered page and show all order data of Customers by from Admin.
"""


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_pending_actions(request):
    storage = messages.get_messages(request)
    storage.used = True

    orders = Order_items.objects.filter(accept_order=True, cancel_return_confirm=True)
    context = {
        "orders": orders,
    }
    return render(request, "admin/admin_order_delivered.html", context)


"""
Get details of Order by Customers from Admin side
"""


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_details_order(request):
    return render(request, "admin/admin_add_order.html")


"""
Edit details of Order by customers from Admin side
"""


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_edit_order(request):
    storage = messages.get_messages(request)
    storage.used = True

    return render(request, "admin/admin_add_order.html")


"""
Order details of Order by customers from Admin side
"""


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def order_details(request, order_id):
    storage = messages.get_messages(request)
    storage.used = True

    order_details = Order_items.objects.get(id=order_id)
    if order_details.status == "Order pending":
        STATUS_CHOICES = None
    elif order_details.status == "Order confirmed":
        STATUS_CHOICES = ("Order confirmed", "Shipped", "Cancelled")
        print(STATUS_CHOICES)
    elif order_details.status == "Shipped":
        STATUS_CHOICES = ("Shipped", "Out For Delivery", "Cancelled")
    elif order_details.status == "Out For Delivery":
        STATUS_CHOICES = ("Out For Delivery", "Delivered", "Cancelled")
    elif order_details.status == "Delivered":
        STATUS_CHOICES = "Returned"
    else:
        STATUS_CHOICES = None

    context = {
        "order_details": order_details,
        "status_choices": STATUS_CHOICES,
    }
    return render(request, "admin/admin_order_details.html", context)


"""
Order details of Order by customers from Admin side
"""


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def order_confirmation(request, order_id):
    storage = messages.get_messages(request)
    storage.used = True

    next_url = request.GET.get("next")
    try:
        order = Order_items.objects.get(id=order_id)
        order_status = order.STATUS_CHOICES
        order.accept_order = True
        order.status = order_status[1][1]
        order.save()
        product_qty = product_sizes_variants.objects.get(
            product_size=order.size, product_data_id=order.product_added
        )
        qty = product_qty.product_quantity
        product_qty.product_quantity = qty - order.quantity
        product_qty.save()
    except Order_items.DoesNotExist:
        messages.error(request, "Could't change status")
    if next_url:
        return redirect(next_url)
    else:
        return redirect("order_processing")


"""
Order details of Order by customers from Admin side
"""


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def order_cancel_approval(request, order_id):
    storage = messages.get_messages(request)
    storage.used = True

    next_url = request.GET.get("next")
    try:
        order = Order_items.objects.get(id=order_id)
        if order.status != "Delivered":
            order_status = order.STATUS_CHOICES
            order.status = order_status[5][1]
            order.save()
        else:
            order_status = order.STATUS_CHOICES
            order.status = order_status[6][1]
            order.save()

        if order.order.payment_method != "cod":
            user_wallet = Wallet_User.objects.get(user_id=order.order.user_id)
            if order.status == "Cancelled":
                user_transactions = Wallet_transactions(
                    wallet_id=user_wallet,
                    amount_received=order.order.total_amount,
                    transaction_for="Order cancelled",
                )
                user_transactions.save()
            else:
                user_transactions = Wallet_transactions(
                    wallet_id=user_wallet,
                    amount_received=order.order.total_amount,
                    transaction_for="Order Returned",
                )
                user_transactions.save()

        product_qty = product_sizes_variants.objects.get(
            product_size=order.size, product_data_id=order.product_added
        )
        qty = product_qty.product_quantity
        product_qty.product_quantity = qty + order.quantity
        product_qty.save()
    except Order_items.DoesNotExist:
        messages.error(request, "Could't change status")
    if next_url:
        return redirect(next_url)
    else:
        return redirect("order_processing")


"""
Order details of Order by customers from Admin side
"""


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def order_status_change(request):
    storage = messages.get_messages(request)
    storage.used = True

    next_url = request.GET.get("next")
    if request.method == "POST":
        status = request.POST.get("status")
        order_id = request.POST.get("order_id")
        try:
            order = Order_items.objects.get(id=order_id)
            order.status = status
            order.save()
            if status == "Cancelled" or status == "Returned":
                order.cancel_return_confirm = False
                order.accept_order = False
                order.save()
                if order.order.payment_method != "cod":
                    user_wallet = Wallet_User.objects.get(user_id=order.order.user_id)
                    user_transactions = Wallet_transactions(
                        wallet_id=user_wallet,
                        amount_received=order.order.total_amount,
                        transaction_for="Order cancelled",
                    )
                    user_transactions.save()

        except Order_items.DoesNotExist:
            messages.error(request, "Could't change status")
    if next_url:
        return redirect(next_url)
    else:
        return redirect("order_processing")


#  <  ===========   USER SIDE  ===========   > #
#  <  ===========   """"""""""""  ===========   > #
#  <  ===========   confirm order pages  ===========   > #


@never_cache
@login_required
def order_confirm(request):
    storage = messages.get_messages(request)
    storage.used = True

    user_id = request.user
    order_serial_number = request.session.get("order_sl_no")

    try:
        user_order = Order.objects.get(
            user_id=user_id, serial_number=order_serial_number
        )
        user_order_items = Order_items.objects.filter(order=user_order)

        context = {
            "user_order": user_order,
            "user_order_items": user_order_items,
        }

        return render(request, "user/order_confirm.html", context)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect("cart_show")


#  <  ===========  End  confirm order  ===========   > #


#  <  ===========   Add order ===========   > #


@login_required
def add_to_order(request):
    storage = messages.get_messages(request)
    storage.used = True

    if not Wallet_User.objects.filter(user_id=request.user).exists():
        Wallet_User.objects.create(user_id=request.user)

    user_in_action = request.user

    if request.POST:
        selected_address = request.POST.get("selected_address")
        amount = float(request.POST.get("amount"))
        payment_mode = request.POST.get("payment_mode")
    else:
        selected_address = request.session["selected_address"]
        amount = float(request.session["amount"])
        payment_mode = request.session["payment_mode"]

    if not selected_address:
        messages.info(request, "Select address or add address")
        return redirect("checkout_product")
    elif not amount and amount != 0.0:
        messages.info(
            request,
            "Error occurred on payment, "
            + "if you cannot solve please contact our customer care.",
        )
        return redirect("checkout_product")
    elif not payment_mode:
        messages.info(
            request,
            "Select a payment, "
            + "if you cannot solve please contact our customer care.",
        )
        return redirect("checkout_product")

    try:
        address = user_address.objects.get(id=selected_address)
        users_cart = Cart.objects.get(user_id=user_in_action)
        users_cart_varients_products = Cart_products.objects.filter(cart=users_cart)

        order_data = Order(
            user_id=user_in_action,
            address=address,
            payment_method=payment_mode,
            total_amount=amount,
        )

        if users_cart.coupon_active:
            order_data.coupon_name = users_cart.coupon.title
            if users_cart.coupon.discount_amount is not None:
                order_data.coupon_discount = "₹ " + str(users_cart.coupon.discount_amount)
            else:
                order_data.coupon_discount = "% " + str(users_cart.coupon.discount_percentage)

        try:
            order_data.full_clean()
            order_data.save()
        except ValidationError as ve:
            messages.error(request, "Order Error: " + str(ve))
            return redirect("cart_show")

        if order_data.payment_method == "wallet":
            user_wallet = Wallet_User.objects.get(user_id=user_in_action)
            user_wallet.balance -= order_data.total_amount
            user_wallet.save()
            wallet_history = Wallet_transactions.objects.create(
                wallet=user_wallet,
                transaction_for="Order using wallet",
                amount_received=Decimal(order_data.total_amount)
            )
            wallet_history.save()

        request.session["order_sl_no"] = str(order_data.serial_number)

        count = 0
        for data in users_cart_varients_products:
            order_item = Order_items(
                order=order_data,
                product_added=data.product_color_variant.product_data_id,
                quantity=data.quantity,
                size=data.product_color_variant.product_size,
                final_product_price=data.sub_total,
                status="Order Pending" if amount != 0.00 else "Payment Pending",
            )
            order_item.save()
            count += 1

        if count > 0:
            users_cart.delete()
            return redirect("order_confirm")

        order_data.delete()
        messages.error(
            request, "Cannot confirm order. Sorry for the inconvenience. Try again."
        )
    except Cart.DoesNotExist:
        messages.error(request, "Cart does not exist.")
        return redirect("cart_show")
    except user_address.DoesNotExist:
        messages.error(
            request, "Selected address not found. Please choose a valid address."
        )
    except Exception as e:
        messages.error(request, "An unexpected error occurred: " + str(e))

    return JsonResponse({"message": "Order could not be processed."})

#  <  ===========   End Add order ===========   > #


#  <  ===========   All User orders  ===========   > #


@never_cache
@login_required
def user_orders(request):
    storage = messages.get_messages(request)
    storage.used = True

    all_orders = Order_items.objects.filter(order__user_id=request.user).order_by(
        "-last_update"
    )
    context = {
        "all_orders": all_orders,
    }
    return render(request, "user/user_orders.html", context)


#  <  ===========   End User orders  ===========   > #


#  <  ===========   All User orders  ===========   > #


@never_cache
@login_required
def user_order_details(request, order_id):
    storage = messages.get_messages(request)
    storage.used = True

    order_details = Order_items.objects.get(id=order_id, order__user_id=request.user)
    other_orders = Order.objects.get(serial_number=order_details.order.serial_number)

    context = {
        "order_details": order_details,
        "other_orders": other_orders,
    }
    return render(request, "user/order_details.html", context)


#  <  ===========   End User orders  ===========   > #

#  <  ===========   Cancel User order  ===========   > #


@login_required
def cancel_order(request, order_id):
    storage = messages.get_messages(request)
    storage.used = True

    next_url = request.GET.get("next")
    try:
        order_item = Order_items.objects.get(id=order_id)
        order_item.cancel_return_confirm = True
        order_item.save()
    except Order_items.DoesNotExist:
        messages.error(request, "Couldn't cancel order, try again")

    messages.success(request, f"Requested to cancel {order_item.product_added}")
    if next_url:
        return redirect(next_url)
    else:
        return redirect("user_orders")


#  <  ===========  END Cancel User order  ===========   > #


#  <  ===========  Invoice User order  ===========   > #
@never_cache
@login_required
def order_invoice(request, serial_number):
    order_details_all = Order_items.objects.filter(order__serial_number=serial_number)
    order_details = Order_items.objects.filter(
        order__serial_number=serial_number
    ).first()
    context = {
        "serial_number": serial_number,
        "order_details": order_details,
        "order_details_all": order_details_all,
    }
    return render(request, "user/invoice.html", context)


#  <  ===========  END Invoice User order  ===========   > #


#  <  ===========  Download Invoice User order  ===========   > #
@never_cache
@login_required
def download_invoice(request, serial_number):
    order_details = Order_items.objects.filter(
        order__serial_number=serial_number
    ).first()
    order_details_all = Order_items.objects.filter(order__serial_number=serial_number)
    context = {"order_details": order_details, "order_details_all": order_details_all}
    template = loader.get_template("user/invoice.html")
    html = template.render(context, request)
    pdf = weasyprint.HTML(string=html).write_pdf()
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="invoice.pdf"'
    response.write(pdf)
    return response


#  <  ===========  Download Invoice User order  ===========   > #
