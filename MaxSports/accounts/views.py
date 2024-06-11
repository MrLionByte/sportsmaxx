from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import user_address, Image as IMG, referral
from order_app.models import Order
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login

from all_validator import views

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your views here.


# =========    Admin Profile handle    =========== #
# =========    ============    =========== #


def user_account_details_admin(request, user_id):
    storage = messages.get_messages(request)
    storage.used = True

    user = User.objects.get(id=user_id)
    addresses = user_address.objects.filter(user=user)

    context = {
        "addresses": addresses,
        "user_data": user,
    }
    return render(request, "admin/admin_user_details.html", context)


# =========    User Profile handle    =========== #
# =========    ============    =========== #

# =========   User profile  =========== #


@login_required
@never_cache
def user_profile(request):
    storage = messages.get_messages(request)
    storage.used = True

    user_obj = request.user
    try:
        addresses = user_address.objects.filter(user=user_obj, delete_address=False)
    except user_address.DoesNotExist:
        addresses = None
    ref = referral.objects.get(user_id=user_obj)
    context = {
        "user_details": user_obj,
        "user_address_details1": addresses,
        "referral": ref,
    }
    return render(request, "user/accounts.html", context)


# =========   End profile  =========== #

# =========   add address details  =========== #


@login_required
def add_account_address(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == "POST":
        username = request.user.username
        user_data = User.objects.get(username=username)

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        alt_phone = request.POST.get("alt_ph")
        pincode = request.POST.get("pincode")
        post_office = request.POST.get("post_office")
        landmark = request.POST.get("landmark")
        accessible = request.POST.get("accessible")
        address_type = request.POST.get("address_type")
        area = request.POST.get("area")
        state = request.POST.get("state")
        city = request.POST.get("city")

        check_full_name = views.name_validator(full_name)
        check_post_office = views.validate_post_office_name(post_office)
        check_pin = views.validate_pin_code(pincode)
        check_landmark = views.validate_landmark(landmark)
        check_accessible = views.validate_area(accessible)
        check_area = views.validate_area(area)
        check_city = views.validate_city(city)
        check_state = views.validate_state(state)
        check_phone = views.validate_phone(phone)
        check_alt_phone = views.validate_phone(alt_phone)

        if check_full_name[0] is True:
            messages.error(request, check_full_name[1])
            return redirect("add_account_address")
        if check_post_office[0] is True:
            messages.error(request, check_post_office[1])
            return redirect("add_account_address")
        if check_pin[0] is True:
            messages.error(request, check_pin[1])
            return redirect("add_account_address")
        if check_landmark[0] is True:
            messages.error(request, check_landmark[1])
            return redirect("add_account_address")
        if check_accessible[0] is True:
            messages.error(request, check_accessible[1])
            return redirect("add_account_address")
        if check_area[0] is True:
            messages.error(request, check_area[1])
            return redirect("add_account_address")
        if check_city[0] is True:
            messages.error(request, check_city[1])
            return redirect("add_account_address")
        if check_state[0] is True:
            messages.error(request, check_state[1])
            return redirect("add_account_address")
        if check_phone[0] is True:
            messages.error(request, check_phone[1])
            return redirect("add_account_address")
        if check_city[0] is True:
            messages.error(request, check_city[1])
            return redirect("add_account_address")
        if check_city[0] is True:
            messages.error(request, check_city[1])
            return redirect("add_account_address")
        if check_alt_phone[0] is True:
            messages.error(request, check_alt_phone[1])
            return redirect("add_account_address")

        data = user_address(
            user=user_data,
            pincode=pincode,
            post_office=post_office,
            landmark=landmark,
            accessible=accessible,
            address_type=address_type,
            area=area,
            state=state,
            city=city,
            alternative_phone=alt_phone,
            phone_no=phone,
            full_name=full_name,
        )
        try:
            data.full_clean()
            data.save()
            messages.success(request, "Address added")
            return redirect("my_account")
        except Exception as e:
            messages.error(request, f"Error! {e}")
    return render(request, "user/add_address.html")


# =========   End address details  =========== #


# =========   Edit address details  =========== #


@login_required
def edit_address(request, address_id):
    storage = messages.get_messages(request)
    storage.used = True

    addresses = user_address.objects.get(id=address_id)
    context = {
        "user_details": addresses,
    }
    if request.method == "POST":

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        alt_phone = request.POST.get("alt_ph")
        pincode = request.POST.get("pincode")
        post_office = request.POST.get("post_office")
        landmark = request.POST.get("landmark")
        accessible = request.POST.get("accessible")
        address_type = request.POST.get("address_type")
        area = request.POST.get("area")
        state = request.POST.get("state")
        city = request.POST.get("city")

        if full_name:
            check_full_name = views.name_validator(full_name)
            if check_full_name[0] is True:
                messages.error(request, check_full_name[1])
                return redirect("add_account_address")
            addresses.full_name = full_name
        if post_office:
            check_post_office = views.validate_post_office_name(post_office)
            if check_post_office[0] is True:
                messages.error(request, check_post_office[1])
                return redirect("add_account_address")
            addresses.post_office = post_office
        if pincode:
            check_pin = views.validate_pin_code(pincode)
            if check_pin[0] is True:
                messages.error(request, check_pin[1])
                return redirect("add_account_address")
            addresses.pincode = pincode
        if landmark:
            check_landmark = views.validate_landmark(landmark)
            if check_landmark[0] is True:
                messages.error(request, check_landmark[1])
                return redirect("add_account_address")
            addresses.landmark = landmark
        if accessible:
            check_accessible = views.validate_area(accessible)
            if check_accessible[0] is True:
                messages.error(request, check_accessible[1])
                return redirect("add_account_address")
            addresses.accessible = accessible
        if area:
            check_area = views.validate_area(area)
            if check_area[0] is True:
                messages.error(request, check_area[1])
                return redirect("add_account_address")
            addresses.area = area
        if city:
            check_city = views.validate_city(city)
            if check_city[0] is True:
                messages.error(request, check_city[1])
                return redirect("add_account_address")
            addresses.city = city
        if state:
            check_state = views.validate_state(state)
            if check_state[0] is True:
                messages.error(request, check_state[1])
                return redirect("add_account_address")
            addresses.state = state
        if phone:
            check_phone = views.validate_phone(phone)
            if check_phone[0] is True:
                messages.error(request, check_phone[1])
                return redirect("add_account_address")
            addresses.phone_no = phone
        if alt_phone:
            check_alt_phone = views.validate_phone(alt_phone)
            if check_alt_phone[0] is True:
                messages.error(request, check_alt_phone[1])
                return redirect("add_account_address")
            addresses.alternative_phone = alt_phone
        if address_type:
            addresses.address_type = address_type

        try:
            addresses.save()
            messages.success(request, "Address updated")
            return redirect("my_account")
        except Exception as e:
            messages.error(request, f"Error ! {e}")

    return render(request, "user/edit_address.html", context)


# =========   End address details  =========== #

# =========  Delete Address =========== #


@login_required
def delete_address(request, address_id):
    storage = messages.get_messages(request)
    storage.used = True

    user_address_to_delete = user_address.objects.get(id=address_id)
    user_address_to_delete.delete_address = True
    user_address_to_delete.save()
    messages.success(request, "Address deleted successfully")
    return redirect("my_account")


# =========  End profile password reset =========== #

# =========   Edit profile details  =========== #


@login_required
def edit_profile(request):
    storage = messages.get_messages(request)
    storage.used = True

    username = request.user.username
    user_data = User.objects.filter(username=username)

    if request.method == "POST":
        user = User.objects.get(username=username)
        user_email = user.email
        user_username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        try:
            if User.objects.filter(username=user_username).exists:
                if username != user_username:
                    raise PermissionDenied("Username already taken.")
            if User.objects.filter(email=email).exists:
                if email != user_email:
                    raise PermissionDenied("Email already taken.")
            if user is not None:
                check_username = views.username_test(username)
                if check_username[0] is True:
                    raise ValidationError(check_username[1])
                user.email = user_email
            if first_name is not None:
                check_F_name = views.name_validator(first_name)
                if check_F_name[0] is True:
                    raise ValidationError(check_F_name[1])
                user.first_name = first_name
            if last_name is not None:
                check_L_name = views.name_validator(last_name)
                if check_L_name[0] is True:
                    raise ValidationError(check_L_name[1])
                user.last_name = last_name
            if email is not None:
                check_email = views.email_test(email)
                if check_email[0] is True:
                    raise ValidationError(check_email[1])
                user.email = email
            user.save()
            messages.success(request, f"Updated {username} successfully")
            return redirect("my_account")

        except PermissionDenied as e:
            messages.error(request, f"Error: {str(e)}")
        except ValidationError as v:
            messages.error(request, f"Error: {str(v)}")

    context = {"user_details": user_data}
    return render(request, "user/edit_accounts.html", context)


# =========     End Edit profile    =========== #

# =========  Edit profile password reset =========== #


@login_required
def change_password(request):
    storage = messages.get_messages(request)
    storage.used = True

    username = request.user.username
    user_obj = User.objects.get(username=username)
    if request.method == "POST":
        old = request.POST["old_pass"]
        new_password = request.POST["new_pass"]
        password_confirm = request.POST["new_passC"]
        if check_password(old, request.user.password):
            pass_check = views.validate_password(new_password)
            if pass_check[0]:
                messages.error(request, pass_check[1])
                return redirect("change_password")
            if new_password != password_confirm:
                messages.error(request, "Password confirmation failed")
                return redirect("change_password")
            else:
                try:
                    user_obj.set_password(new_password)
                    user_obj.save()
                    messages.success(request, "Password changed successfully")
                    return redirect("my_account")
                except TypeError:
                    user_object = authenticate(
                        request, username=username, password=new_password
                    )
                    login(request, user_object)
                    messages.success(request, "Password changed successfully")
                    return redirect("my_account")
        else:
            messages.error(request, "Incorrect password")
            return redirect("change_password")

    return render(request, "user/change_password.html")


# =========  End profile password reset =========== #

# ========= Checkout  add address details  =========== #


@login_required
def add_checkout_address(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == "POST":
        username = request.user.username
        user_data = User.objects.get(username=username)

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        alt_phone = request.POST.get("alt_ph")
        pincode = request.POST.get("pincode")
        post_office = request.POST.get("post_office")
        landmark = request.POST.get("landmark")
        accessible = request.POST.get("accessible")
        address_type = request.POST.get("address_type")
        area = request.POST.get("area")
        state = request.POST.get("state")
        city = request.POST.get("city")

        check_full_name = views.name_validator(full_name)
        check_post_office = views.validate_post_office_name(post_office)
        check_pin = views.validate_pin_code(pincode)
        check_landmark = views.validate_landmark(landmark)
        check_accessible = views.validate_area(accessible)
        check_area = views.validate_area(area)
        check_city = views.validate_city(city)
        check_state = views.validate_state(state)
        check_phone = views.validate_phone(phone)
        check_alt_phone = views.validate_phone(alt_phone)

        if check_full_name[0] is True:
            messages.error(request, check_full_name[1])
            return redirect("add_account_address")
        if check_post_office[0] is True:
            messages.error(request, check_post_office[1])
            return redirect("add_account_address")
        if check_pin[0] is True:
            messages.error(request, check_pin[1])
            return redirect("add_account_address")
        if check_landmark[0] is True:
            messages.error(request, check_landmark[1])
            return redirect("add_account_address")
        if check_accessible[0] is True:
            messages.error(request, check_accessible[1])
            return redirect("add_account_address")
        if check_area[0] is True:
            messages.error(request, check_area[1])
            return redirect("add_account_address")
        if check_city[0] is True:
            messages.error(request, check_city[1])
            return redirect("add_account_address")
        if check_state[0] is True:
            messages.error(request, check_state[1])
            return redirect("add_account_address")
        if check_phone[0] is True:
            messages.error(request, check_phone[1])
            return redirect("add_account_address")
        if check_city[0] is True:
            messages.error(request, check_city[1])
            return redirect("add_account_address")
        if check_city[0] is True:
            messages.error(request, check_city[1])
            return redirect("add_account_address")
        if check_alt_phone[0] is True:
            messages.error(request, check_alt_phone[1])
            return redirect("add_account_address")

        data = user_address(
            user=user_data,
            pincode=pincode,
            post_office=post_office,
            landmark=landmark,
            accessible=accessible,
            address_type=address_type,
            area=area,
            state=state,
            city=city,
            alternative_phone=alt_phone,
            phone_no=phone,
            full_name=full_name,
        )
        try:
            data.full_clean()
            data.save()
            messages.success(request, "Address added")
            return redirect("checkout_product")
        except Exception as e:
            messages.error(request, f"Error ! {e}")
    return render(request, "user/add_address.html")


# =========  Checkout End address details  =========== #

# =========  Checkout Edit address  =========== #


@login_required
def edit_checkout_address(request, address_id):
    storage = messages.get_messages(request)
    storage.used = True

    addresses = user_address.objects.get(id=address_id)
    context = {
        "user_details": addresses,
    }

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        alt_phone = request.POST.get("alt_ph")
        pincode = request.POST.get("pincode")
        post_office = request.POST.get("post_office")
        landmark = request.POST.get("landmark")
        accessible = request.POST.get("accessible")
        address_type = request.POST.get("address_type")
        area = request.POST.get("area")
        state = request.POST.get("state")
        city = request.POST.get("city")

        if full_name:
            check_full_name = views.name_validator(full_name)
            if check_full_name[0] is True:
                messages.error(request, check_full_name[1])
                return redirect("add_account_address")
            addresses.full_name = full_name
        if post_office:
            check_post_office = views.validate_post_office_name(post_office)
            if check_post_office[0] is True:
                messages.error(request, check_post_office[1])
                return redirect("add_account_address")
            addresses.post_office = post_office
        if pincode:
            check_pin = views.validate_pin_code(pincode)
            if check_pin[0] is True:
                messages.error(request, check_pin[1])
                return redirect("add_account_address")
            addresses.pincode = pincode
        if landmark:
            check_landmark = views.validate_landmark(landmark)
            if check_landmark[0] is True:
                messages.error(request, check_landmark[1])
                return redirect("add_account_address")
            addresses.landmark = landmark
        if accessible:
            check_accessible = views.validate_area(accessible)
            if check_accessible[0] is True:
                messages.error(request, check_accessible[1])
                return redirect("add_account_address")
            addresses.accessible = accessible
        if area:
            check_area = views.validate_area(area)
            if check_area[0] is True:
                messages.error(request, check_area[1])
                return redirect("add_account_address")
            addresses.area = area
        if city:
            check_city = views.validate_city(city)
            if check_city[0] is True:
                messages.error(request, check_city[1])
                return redirect("add_account_address")
            addresses.city = city
        if state:
            check_state = views.validate_state(state)
            if check_state[0] is True:
                messages.error(request, check_state[1])
                return redirect("add_account_address")
            addresses.state = state
        if phone:
            check_phone = views.validate_phone(phone)
            if check_phone[0] is True:
                messages.error(request, check_phone[1])
                return redirect("add_account_address")
            addresses.phone_no = phone
        if alt_phone:
            check_alt_phone = views.validate_phone(alt_phone)
            if check_alt_phone[0] is True:
                messages.error(request, check_alt_phone[1])
                return redirect("add_account_address")
            addresses.alternative_phone = alt_phone
        if address_type:
            addresses.address_type = address_type

        try:
            addresses.save()
            messages.success(request, "Address updated")
            return redirect("checkout_product")
        except Exception as e:
            messages.error(request, f"Error ! {e}")

    return render(request, "user/edit_address.html", context)


# =========  End Checkout Edit address =========== #
