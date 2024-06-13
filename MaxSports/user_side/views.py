from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import re
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from MaxSports.settings import EMAIL_HOST_USER
import random
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from accounts.models import referral
from wallet.models import Wallet_User, Wallet_transactions
from all_validator import views

# Create your views here.

# Check Type
email_type = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
user_type = "^[A-Za-z][A-Za-z0-9_]{5,29}$"
# End Check Type


# =========  SIGN-UP  =========== #
@never_cache
def user_sign_up(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        referral_code = request.POST.get("referral")

        check_Fname = views.name_validator(firstname)
        check_email = views.email_test(email)
        check_username = views.username_test(username)
        check_password = views.validate_password(password)

        try:
            if password != password_confirm:
                messages.error(request, "Password confirmation failed!!")
                return redirect("user_sign_up")
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already registered")
                return redirect("user_sign_up")
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already registered")
                return redirect("user_sign_up")
            if check_username[0] is True:
                messages.error(request, check_username[1])
                return redirect("user_sign_up")
            if check_Fname[0] is True:
                messages.error(request, check_Fname[1])
                return redirect("user_sign_up")
            if check_email[0] is True:
                messages.error(request, check_email[1])
                return redirect("user_sign_up")
            if check_password[0] is True:
                messages.error(request, check_password[1])
                return redirect("user_sign_up")
            if referral_code:
                check = referral.objects.filter(referral_code=referral_code).exists()
                if check is False:
                    messages.error(request, "Referral code invalid")
                    return redirect("user_sign_up")

            request.session["firstname"] = firstname
            if lastname:
                request.session["lastname"] = lastname
            request.session["email"] = email
            request.session["username"] = username
            request.session["password"] = password
            if referral_code:
                request.session["referral_code"] = referral_code
            email_otp_generator(email, request)
            return redirect("otp_reg")
        except ValueError as e:
            messages.info(request, str(e))
        except Exception as s:
            messages.error(request, f"Error occurred,Try again !!{s}")
    return render(request, "user/sign_up.html")


# =========  END SIGN-UP  =========== #


# =========  MOBILE OTP  =========== #

# @api_view
# def send_otp(request):
#         data = request.data

#         if data.get('phone_number') is None:
#                 return Response ({
#                         'status' : 400
#                         'message' : 'Key phone number is required'
#                 })

#         if data.get('password') is None:
#                 return Response ({
#                         'status' : 400
#                         'message' : 'Key password is required'
#                 })
#         phone = data.get('phone')
#         otp = send_otp_phone(data.get('phone'))
#         user = User.objects.create(phone = phone)
#         user.set_password = data.get('set_password')

# =========  END MOBILE OTP  =========== #


# ========= EMAIL OTP GENERATOR =========== #
def email_otp_generator(email, request=None):
    otp = random.randint(100000, 999999)
    expires_timer_otp = datetime.now() + timedelta(minutes=2)
    if request.session.get("username"):
        user = request.session.get("username")
    else:
        user = request.session.get("username_for_forgot_password")
    message1 = f"Dear {user} Your OTP for verification : {otp}"
    message2 = "Thank You for being part of Sports_Maxx "
    send_mail(
        subject="Your OTP for verification",
        message=message1 + message2,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True,
    )

    if request:
        request.session["expires_timer_otp"] = expires_timer_otp.isoformat()
        request.session["otp"] = otp


# ========= END OTP GENERATOR  =========== #


# ========= OTP RESEND GENERATOR =========== #


@never_cache
def resend_otp(request):
    otp = random.randint(100000, 999999)
    expires_timer_otp = datetime.now() + timedelta(minutes=2)
    email = request.session.get("email")
    user = request.session.get("username")

    send_mail(
        subject="Resend OTP for verification",
        message=(
            f"Dear {user} Your new OTP for verification is:"
            + f"{otp}  Thank You for being part of Sports_Maxx"
        ),
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True,
    )

    if request:
        request.session["expires_timer_otp"] = expires_timer_otp.isoformat()
        request.session["otp"] = otp

    return redirect("otp_reg")


# ========= END RESEND GENERATOR =========== #


# =========  EMAIL OTP VERIFICATION AND SAVE  =========== #
@never_cache
def otp_reg(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == "POST":
        input_otp = request.POST.get("otp_input")
        check_otp = request.session.get("otp")
        expires_timer_otp = request.session.get("expires_timer_otp")

        if expires_timer_otp < datetime.now().isoformat():
            storage = messages.get_messages(request)
            storage.used = True
            messages.error(request, "OTP Time out")

        elif int(input_otp) == int(check_otp):
            first_name = request.session.get("firstname")
            last_name = request.session.get("lastname")
            email = request.session.get("email")
            user_name = request.session.get("username")
            password = request.session.get("password")
            referral_code = request.session.get("referral_code")

            user = User.objects.create_user(user_name, email, password)
            if last_name:
                user.last_name = last_name
            user.first_name, user.last_name = first_name, last_name
            user.save()

            wallet_user = Wallet_User.objects.create(user_id=user)
            if referral_code:
                wallet_user.balance = 50
            wallet_user.save()
            if referral_code:
                wallet_history = Wallet_transactions.objects.create(
                    wallet_id=wallet_user, transaction_for="Referral"
                )
                wallet_history.save()
                referral_obj = referral.objects.get(referral_code=referral_code)
                wallet = Wallet_User.objects.get(user_id=referral_obj.user)
                wallet.balance = wallet.balance + 150
                wallet.save()
                wallet_history = Wallet_transactions.objects.create(
                    wallet_id=wallet, transaction_for="Referral"
                )
                wallet_history.save()

            storage = messages.get_messages(request)
            storage.used = True
            messages.success(request, "User created successfully")
            return redirect("user_sign_up")

        else:

            messages.error(request, "OTP is mismatching")

    return render(request, "user/otp_reg.html")


# ========= END EMAIL OTP VERIFICATION AND SAVE =========== #


# =========     SIGN-IN          =========== #


@never_cache
def user_sign_in(request):
    storage = messages.get_messages(request)
    storage.used = True

    flag = 0
    if request.method == "POST":
        check_name = request.POST.get("username")
        password = request.POST.get("password")
        try:

            try:
                user_object = authenticate(
                    request, username=check_name, password=password
                )
                if user_object is None:
                    raise User.DoesNotExist
            except User.DoesNotExist:
                user = User.objects.get(email=check_name)
                user_object = authenticate(
                    request, username=user.username, password=password
                )

            if user_object is not None:
                login(request, user_object)
                return redirect("home")

            elif User.objects.filter(username=check_name, is_active=True).exists():
                # request.session['username_for_forgot_password'] = check_name
                request.session["username"] = check_name
                x = request.session.get("username")
                messages.info(request, "Password is incorrect ")
                flag = 1
            elif User.objects.filter(username=check_name, is_active=False).exists():
                messages.error(request, "You Got blocked")
            elif User.objects.filter(email=check_name, is_active=False).exists():
                messages.error(request, "You Got blocked")
            else:
                messages.error(request, "unable to find user ,check the credentials")
        except ValueError as e:
            messages.info(request, str(e))
    if flag == 1:
        passed = True
    else:
        passed = False
    return render(request, "user/login.html", {"passed": passed})


# =========    END SIGN-IN    =========== #

# =========    Forgot Password email verify   =========== #


@never_cache
def forgot_password_email(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == "POST":
        try:
            email = request.POST.get("email")
            username = request.session.get("username")
            user = User.objects.get(username=username)
            if user.email == email:
                request.session["email"] = email
                forgot_password_otp(request)
                return redirect("forgot_password")
        except User.DoesNotExist:
            messages.error(request, "Email doesn't match,try again")
        except KeyError:
            messages.error(request, "Could proceed, Try forgot password again")
    return render(request, "user/forgot_pass.html")


# =========    Forgot Password email verify   =========== #


# ========= OTP RESEND GENERATOR =========== #


@never_cache
def forgot_password_otp(request):
    otp = random.randint(100000, 999999)
    expires_timer_otp = datetime.now() + timedelta(minutes=5)

    email = request.session.get("email")
    user = request.session.get("username")

    send_mail(
        subject="OTP for forgot password reset",
        message=(
            f"Dear {user} Your OTP for password reset is:"
            + f"{otp}  Thank You for being part of Sports_Maxx."
            + "Don't Share the OTP with anyone."
            + "If you haven't initiated this request please contact us!"
        ),
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True,
    )

    if request:
        request.session["expires_timer_otp"] = expires_timer_otp.isoformat()
        request.session["otp"] = otp

    return redirect("forgot_password")


# ========= END RESEND GENERATOR =========== #


# =========    Forgot Password    =========== #


@never_cache
def forgot_password(request):
    storage = messages.get_messages(request)
    storage.used = True

    expires_timer_otp = request.session.get("expires_timer_otp")
    otp = int(request.session.get("otp"))
    context = {
        "user_data": True,
    }

    if request.method == "POST":
        password = request.POST.get("password_new")
        confirm_password = request.POST.get("password_conf")
        input_otp = int(request.POST.get("otp_input"))

        check_password = views.validate_password(password)
        if expires_timer_otp < datetime.now().isoformat():
            storage = messages.get_messages(request)
            storage.used = True
            messages.error(request, "OTP Time out")
        elif otp != input_otp:
            messages.error(request, "OTP mismatches try again!!")
        elif check_password[0] is True:
            messages.error(request, check_password[1])
        elif password == confirm_password:
            try:
                username = request.session.get("username")
                user_obj = User.objects.get(username=username)
                user_obj.set_password(password)
                user_obj.save()
                messages.success(request, "Password reset successful. Please sign in.")
                return redirect("user_sign_in")
            except TypeError:
                messages.success(request, "Password reset successful. Please sign in.")
                return redirect("user_sign_in")
        else:
            messages.error(request, "Password confirmation failed")
    return render(request, "user/forgot_pass.html", context)


# =========    Forgot Password    =========== #

# =========    END LOG-OUT    =========== #


@login_required
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")
    return redirect("home")


# =========    END LOG-OUT    =========== #
