from django.shortcuts import render, redirect
from banner_app.models import sub_banner, main_banner
from product_app.models import product_color_image
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import user_passes_test


# Create your views here.


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def show_banner(request):
    storage = messages.get_messages(request)
    storage.used = True

    sub = sub_banner.objects.all()
    main = main_banner.objects.all()

    context = {
        "sub_banner": sub,
        "main_banner": main,
    }
    return render(request, "admin/admin_banner.html", context)


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def add_banner(request):
    storage = messages.get_messages(request)
    storage.used = True

    product = product_color_image.objects.all()
    try:
        banner_name = request.GET.get("banner_name")
        product_selected = request.GET.get("product")
        product_description = request.GET.get("product_description")
        expiry = request.GET.get("expiry")
        start = request.GET.get("start")

        product_selected = product_color_image.objects.get(id=product_selected)
        banner = main_banner(
            name=banner_name,
            product=product_selected,
            description=product_description,
            expiry=expiry,
            start=start,
        )

        banner.full_clean()
        banner.save()
        messages.success(request, "Banner added")
    except ValidationError:
        messages.error(request, "Error occurred, Try again")
    except product_color_image.DoesNotExist:
        pass
    context = {
        "product": product,
    }

    return render(request, "admin/admin_banner_add.html", context)


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def list_banner(request):
    banner_id = request.GET.get("banner_id")
    banner = main_banner.objects.get(id=banner_id)
    banner.status = True
    banner.save()
    messages.success(request, f"Banner {banner} Listed")
    return redirect("show_banner")


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def unlist_banner(request):
    banner_id = request.GET.get("banner_id")
    banner = main_banner.objects.get(id=banner_id)
    banner.status = False
    banner.save()
    messages.success(request, f"Banner {banner} Listed")
    return redirect("show_banner")


def edit_banner(request):
    pass
