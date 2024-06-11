from django.shortcuts import render, redirect
from django.contrib import messages
from .models import category, available_types
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from all_validator import views


# Create your views here.

#       <<< == ==  ADMIN  == == >>>

# ========  Admin Category ======== #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_category(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.user.is_superuser:
        category_data = category.objects.filter(category_delete=True).order_by(
            "id", "category_name"
        )
        context = {"category_data": category_data}
        return render(request, "admin/admin_category.html", context)
    return redirect("admin_login")


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_category_unlisted(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.user.is_superuser:
        category_data = category.objects.filter(category_delete=False).order_by(
            "id", "category_name"
        )
        context = {"category_data": category_data}
        return render(request, "admin/admin_category_unlisted.html", context)
    return redirect("admin_login")


# ========  Add New Category ======== #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_add_category(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.user.is_superuser:
        if request.method == "POST":
            category_name = request.POST.get("categoryName")
            category_name = category_name.upper()
            cat_available_types = request.POST.get("available_types")
            cat_types = available_types.objects.get(pk=cat_available_types)
            category_image = request.FILES.get("category_avatar")
            if not views.is_image(category_image.name):
                messages.error(request, "Only image is allowed")
                return redirect("admin_add_category")
            check = views.name_test(category_name)
            if category.objects.filter(category_name=category_name).exists():
                messages.error(request, "Category already exist")
                return redirect("admin_add_category")
            elif check[0] is True:
                messages.error(request, check[1])
                return redirect("admin_add_category")
            new_category = category(
                category_name=category_name,
                category_image=category_image,
                types_available=cat_types.type,
            )
            try:
                new_category.full_clean()
                new_category.save()
                return redirect("admin_category")

            except ValidationError:
                messages.error(request, "Validation Error")
        context = {"available_types": available_types.objects.all()}
        return render(request, "admin/admin_category_add.html", context)
    return redirect("admin_login")


# ========  EDIT   Category ======== #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_edit_category(request, category_id):
    storage = messages.get_messages(request)
    storage.used = True

    context = {"category_data": category.objects.filter(pk=category_id)}
    if request.method == "POST":
        try:
            category_data = category.objects.get(pk=category_id)
            category_name = request.POST.get("categoryName")
            category_image = request.FILES.get("category_avatar")

            if category_name:
                check_error = views.name_test(category_name)
                category_name = category_name.upper()
                if check_error[0] is True:
                    message = check_error[1]
                    messages.error(request, message)
                    return redirect("admin_edit_category")
                elif category.objects.filter(category_name=category_name).exists():
                    messages.error(request, "Category already exist")
                    return redirect("admin_edit_category")
                category_data.category_name = category_name

            if category_image:
                if not views.is_image(category_image.name):
                    messages.error(request, "Only image is allowed")
                    return redirect("admin_edit_category")
                category_data.category_image = category_image

            category_data.save()
            return redirect("admin_category")
        except category.DoesNotExist:
            return redirect("admin_category")

    return render(request, "admin/admin_category_edit.html", context)


# ========  List/Unlist Category ======== #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_List_category(request, category_id):
    try:
        action_on_user = category.objects.get(id=category_id)
    except category.DoesNotExist:
        return redirect("admin_category")
    action_on_user.is_listed = True
    action_on_user.save()
    return redirect("admin_category")


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_UnList_category(request, category_id):
    try:
        action_on_user = category.objects.get(id=category_id)
    except category.DoesNotExist:
        return redirect("admin_category")
    action_on_user.is_listed = False
    action_on_user.save()
    return redirect("admin_category")


# ========  DELETE Category ======== #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_delete_category(request, category_id):

    try:
        delete_category = category.objects.get(pk=category_id)
    except category.DoesNotExist:
        return redirect("admin_category")
    delete_category.category_delete = True
    delete_category.save()
    return redirect("admin_category_unlisted")


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_undo_category(request, category_id):

    try:
        delete_category = category.objects.get(pk=category_id)
    except category.DoesNotExist:
        return redirect("admin_category")
    delete_category = category.objects.get(pk=category_id)
    delete_category.category_delete = False
    delete_category.save()
    return redirect("admin_category")


# ========  Admin Variant ======== #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_types_for_category(request):
    storage = messages.get_messages(request)
    storage.used = True

    context = {"type_data": available_types.objects.all()}
    return render(request, "admin/admin_category_type.html", context)


# ========  Admin Add Variant ======== #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_add_types_for_category(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == "POST":
        type = request.POST.get("type")
        if type is not None:
            save_type = available_types(type=type)
            save_type.save()
    return render(request, "admin/admin_category_type_add.html")


#   <<< == ==  END ADMIN  == == >>>
