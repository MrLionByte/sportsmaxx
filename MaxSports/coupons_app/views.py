from django.shortcuts import render, redirect
from django.contrib import messages
from coupons_app.models import Coupons
import random
import string
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from all_validator import views

# Create your views here.
date_now = (timezone.now()).date()


# < =======    COUPON  GENERATOR    ======= >


def generate_coupons(string_length=5, number_length=5):
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=string_length)
    )
    random_number = "".join(random.choices(string.digits, k=number_length))
    random_coupon_code = random_string + random_number
    if not Coupons.objects.filter(code=random_coupon_code).exists():
        return random_coupon_code


# < =======    END GENERATOR COUPON      ======= >

# < =======    Admin Show COUPON      ======= >


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_coupons(request):
    storage = messages.get_messages(request)
    storage.used = True

    all_coupons = Coupons.objects.filter(expiry__gte=date_now).order_by("expiry")
    return render(request, "admin/admin_coupon.html", {"all_coupons": all_coupons})


# < =======    End Show COUPON      ======= >


# < =======    ADD COUPON      ======= >


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_coupon_add(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == "POST":
        coupon_title = request.POST.get("coupon_title")
        min_price = request.POST.get("min_price")
        max_price = request.POST.get("max_price")
        serial_code = request.POST.get("code")
        valid = request.POST.get("valid")
        expiry = request.POST.get("expiry")
        discountPercentage = request.POST.get("discountPercentage")
        choice = request.POST.get("choice")
        check_title = views.name_test(coupon_title)
        if check_title[0] is True:
            messages.error(request, check_title[1])
            return redirect("admin_coupon_add")
        if valid < str(date_now):
            messages.error(request, "Give proper Valid From date")
            return redirect("admin_coupon_add")
        if expiry <= valid:
            messages.error(request, "Give proper expiry and valid date")
            return redirect("admin_coupon_add")
        elif float(min_price) > float(max_price):
            messages.error(request, "Minimum price must be less than Maximum")
            return redirect("admin_coupon_add")
        if not serial_code:
            serial_code = generate_coupons()
        else:
            serial_code = serial_code.upper()
            check_code = views.couponcode_validate(serial_code)
            if check_code[0] is True:
                messages.error(request, check_code[1])
                return redirect("admin_coupon_add")

        coupon = Coupons(
            title=coupon_title,
            code=serial_code,
            valid_from=valid,
            expiry=expiry,
            max_limit=max_price,
            min_limit=min_price,
        )
        if choice == "amt":
            if float(discountPercentage) > float(max_price) or float(
                discountPercentage
            ) > float(min_price):
                messages.error(
                    request, "Discount amount should be less than minimum limit"
                )
                return redirect("admin_coupon_add")
            coupon.discount_amount = discountPercentage
        else:
            check_percentage = views.percentage_validator(discountPercentage)
            if check_percentage[0] is True:
                messages.error(request, check_percentage[1])
                return redirect("admin_coupon_add")
            coupon.discount_percentage = discountPercentage
        try:
            coupon.full_clean
            coupon.save()
            messages.success(request, "Coupon Added Successfully")
        except ModuleNotFoundError:
            messages.error(request, "Try again, Error occurred")

    return render(request, "admin/admin_coupons_add.html")


# < =======  END ADD COUPON   ======= >


# < =======  LIST/UNLIST COUPON   ======= >


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def coupon_list(request, coupon_id):
    try:
        coupon = Coupons.objects.get(id=coupon_id)
        coupon.is_active = True
        coupon.save()
        messages.success(request, f"Listed Coupon {coupon.title}")
        return redirect("admin_coupons")
    except Coupons.DoesNotExist:
        messages.error(request, "Error occurred")
    return redirect("admin_coupons")


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def coupon_un_list(request, coupon_id):
    try:
        coupon = Coupons.objects.get(id=coupon_id)
    except Coupons.DoesNotExist:
        return redirect("admin_coupons")
    coupon.is_active = False
    coupon.save()
    messages.success(request, f"Unlisted Coupon {coupon.title}")
    return redirect("admin_coupons")


# < =======  END LIST/UNLIST COUPON   ======= >


# < =======  Expired COUPON   ======= >


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def coupons_expired(request):
    storage = messages.get_messages(request)
    storage.used = True

    all_coupons = Coupons.objects.filter(expiry__lte=date_now).order_by("expiry")
    context = {
        "all_coupons": all_coupons,
    }
    return render(request, "admin/admin_coupon_expired.html", context)


# < ======= END Expired COUPON ======= >


# < =======  Edit COUPON   ======= >


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def edit_coupon(request, coupon_id):
    storage = messages.get_messages(request)
    storage.used = True

    next_url = request.GET.get("next")
    coupon = Coupons.objects.get(id=coupon_id)
    context = {"coupon": coupon, "coupon_id": coupon_id}

    if request.method == "POST":
        coupon_title = request.POST.get("title")
        min_price = request.POST.get("min")
        max_price = request.POST.get("max")
        valid = request.POST.get("valid")
        expiry = request.POST.get("expiry")
        discountPercentage = request.POST.get("discountPercentage")
        choice = request.POST.get("choice")
        try:
            if coupon_title is not None:
                check_title = views.name_test(coupon_title)
                if check_title[0] is True:
                    messages.error(request, check_title[1])
                    return redirect(next_url, coupon_id)
                coupon.title = coupon_title
            if min_price is not None:
                if float(min_price) > float(max_price):
                    messages.error(request, "Min price should be less than max price")
                    return redirect(next_url, coupon_id)
                check_min = views.price_test(min_price)
                if check_min[0] is True:
                    messages.error(request, check_min[1])
                    return redirect(next_url, coupon_id)
                coupon.min_limit = min_price
            if max_price is not None:
                if float(max_price) < float(min_price):
                    messages.error(request, "Min price should be less than max price")
                    return redirect(next_url, coupon_id)
                check_max = views.price_test(max_price)
                if check_max[0] is True:
                    messages.error(request, check_max[1])
                    return redirect(next_url, coupon_id)
                coupon.max_limit = max_price
            if valid is not None:
                if valid < str(date_now):
                    messages.error(request, "Give proper Valid From date")
                    return redirect(next_url)
                elif valid > expiry:
                    messages.error(request, "valid date should be less than expiry")
                    return redirect(next_url)
                coupon.valid_from = valid
            if expiry is not None:
                if expiry <= str(date_now):
                    messages.error(request, "Give proper Expiry date")
                    return redirect(next_url)
                elif valid > expiry:
                    messages.error(request, "valid date should be less than expiry")
                    return redirect(next_url)
                coupon.expiry = expiry

            if discountPercentage is not None:
                if choice == "per":
                    check_discountPer = views.percentage_validator(discountPercentage)
                    if check_discountPer[0] is True:
                        messages.error(request, check_discountPer[1])
                        return redirect(next_url)
                    else:
                        check_discountAmt = views.price_test(discountPercentage)
                        if check_discountAmt[0] is True:
                            messages.error(request, check_discountAmt[1])
                            return redirect(next_url)
                        coupon.discount_percentage = discountPercentage
                else:
                    if float(discountPercentage) > float(max_price) or float(
                        discountPercentage
                    ) > float(min_price):
                        messages.error(
                            request, "Discount is should be less than minimum price"
                        )
                        return redirect(next_url)
                    coupon.discount_amount = discountPercentage
            coupon.save()
            messages.success(request, f"Edited {coupon_title} successfully")
        except Coupons.DoesNotExist:
            return redirect(next_url)

    return render(request, "admin/admin_coupon_edit.html", context)


# < ======= END Edit COUPON ======= >
