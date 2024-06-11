from django.shortcuts import render, redirect

# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import products, product_color_image, product_sizes_variants
from category_app.models import category
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.db.models import Q
from all_validator.views import is_image, name_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from order_app.models import Order_items
from all_validator import views

# from django.db.models import Subquery, OuterRef, FloatField

# Create your views here.

# ========  Admin Show Product ======== #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_product(request):
    storage = messages.get_messages(request)
    storage.used = True

    search_query = request.POST.get("search", "")
    if search_query:
        products_data = products.objects.filter(
            Q(product_name__icontains=search_query, product_delete=False)
        )
    else:
        try:
            sort_id = request.GET.get("sort_id", None)
            sort_id = int(sort_id)
            if sort_id == 1:
                products_data = products.objects.filter(product_delete=False).order_by(
                    "product_name"
                )
            elif sort_id == 2:
                products_data = products.objects.filter(product_delete=False).order_by(
                    "product_added_at"
                )
            elif sort_id == 3:
                products_data = products.objects.filter(product_delete=False).order_by(
                    "category_id"
                )
            elif sort_id == 4:
                products_data = products.objects.filter(product_delete=False).order_by(
                    "-product_price"
                )
            elif sort_id == 5:
                products_data = products.objects.filter(product_delete=False).order_by(
                    "product_price"
                )
        except TypeError:
            products_data = products.objects.filter(product_delete=False).order_by("id")

    context = {
        "products_data": products_data,
    }
    return render(request, "admin/admin_product.html", context)


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_product_unlisted(request):
    storage = messages.get_messages(request)
    storage.used = True

    search_query = request.POST.get("search", "")
    if search_query:
        products_data = products.objects.filter(
            Q(product_name__icontains=search_query, product_delete=True)
        )
    else:
        try:
            sort_id = request.GET.get("sort_id", None)
            sort_id = int(sort_id)
            if sort_id == 1:
                products_data = products.objects.filter(product_delete=True).order_by(
                    "product_name"
                )
            elif sort_id == 2:
                products_data = products.objects.filter(product_delete=True).order_by(
                    "product_added_at"
                )
            elif sort_id == 3:
                products_data = products.objects.filter(product_delete=True).order_by(
                    "category_id"
                )
            elif sort_id == 4:
                products_data = products.objects.filter(product_delete=True).order_by(
                    "product_price"
                )
            elif sort_id == 5:
                products_data = products.objects.filter(product_delete=True).order_by(
                    "-product_price"
                )
        except TypeError:
            products_data = products.objects.filter(product_delete=True).order_by("id")

    context = {
        "products_data": products_data,
    }
    return render(request, "admin/admin_product_unlisted.html", context)


# ========  END Show Product ======== #

# ========  Admin Add Product ======== #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_add_product(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == "POST":
        product_name = request.POST.get("product_name")
        category_id = request.POST.get("selected_category")
        price = request.POST.get("price")
        offer_percentage = request.POST.get("offer_percentage")
        product_des = request.POST.get("product_description")

        try:
            check_product = views.name_test(product_name)
            check_price = views.price_test(price)
            check_offer = views.percentage_validator(offer_percentage)
            check_description = views.description_validator(product_des)

            if check_product[0] is True:
                messages.error(request, check_product[1])
            elif check_price[0] is True:
                messages.error(request, check_price[1])
            elif check_offer[0] is True:
                messages.error(request, check_offer[1])
            elif check_description[0] is True:
                messages.error(request, check_description[1])
            else:
                cat = category.objects.get(id=category_id)
                product_data = products(
                    product_name=product_name,
                    category_id=cat,
                    product_price=price,
                    offer_percentage=offer_percentage,
                    product_description=product_des,
                )
                product_data.full_clean()
                product_data.save()
                messages.success(request, "Product created successfully")
                return redirect("admin_add_product")

        except category.DoesNotExist:
            messages.error(request, "Category does not exist")
        except ValueError:
            messages.error(request, "Invalid input value")
        except Exception as e:
            messages.error(request, "An error occurred: {}".format(e))
    context = {"categories": category.objects.all()}
    return render(request, "admin/admin_product_add.html", context)


# ========  END Add Product ======== #

# ========  Admin Details Product ======== #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_details_product(request, product_id):
    storage = messages.get_messages(request)
    storage.used = True

    if request.user.is_superuser:

        product_data = product_color_image.objects.filter(product_id__pk=product_id)
        context = {
            "product_name": products.objects.get(pk=product_id),
            "product_data": product_data,
        }
        return render(request, "admin/admin_product_details.html", context)
    return redirect("admin_login")


# ========  END  Details Product ======== #


# ========  Feature/Un_feature Product ======== #
@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def feature(request, product_id):

    next_url = request.GET.get("next")
    try:
        action_on_user = product_color_image.objects.get(id=product_id)
    except product_color_image.DoesNotExist:
        return redirect(next_url)
    action_on_user.featured = True
    action_on_user.save()
    return redirect(next_url)


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def unfeature(request, product_id):
    next_url = request.GET.get("next")
    try:
        action_on_user = product_color_image.objects.get(id=product_id)
    except product_color_image.DoesNotExist:
        return redirect(next_url)
    action_on_user.featured = False
    action_on_user.save()
    return redirect(next_url)


# ======  End Feature/Un_feature Product ======= #


# ========  Delete/Undo Product ======== #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_list_product(request, product_id):
    try:
        action_on_user = products.objects.get(id=product_id)
    except products.DoesNotExist:
        return redirect("admin_product")
    action_on_user.product_delete = False
    action_on_user.save()
    return redirect("admin_product_unlisted")


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_unlist_product(request, product_id):
    try:
        action_on_user = products.objects.get(id=product_id)
    except products.DoesNotExist:
        return redirect("admin_product")
    action_on_user.product_delete = True
    action_on_user.save()
    return redirect("admin_product")


# ========  End Delete/Undo Product  ======== #


# ========  Status (List/Unlist) Product ======== #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_productStatus_list(request, product_id):
    try:
        action_on_product = products.objects.get(id=product_id)
        action_on_product.product_list = True
        action_on_product.save()
    except products.DoesNotExist:
        pass
    return redirect("admin_product")


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_productStatus_unlist(request, product_id):
    try:
        action_on_product = products.objects.get(id=product_id)
        action_on_product.product_list = False
        action_on_product.save()
    except products.DoesNotExist:
        pass
    return redirect("admin_product")


# ========  End Status (List/Unlist) Product  ======== #

# ========  Color Delete/Undo Product ======== #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def product_color_delete(request, product_id):
    next_url = request.GET.get("next")
    try:
        action_on_user = product_color_image.objects.get(id=product_id)
    except product_color_image.DoesNotExist:
        return redirect(next_url)
    action_on_user.delete_opt = False
    action_on_user.save()
    return redirect(next_url)


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def product_color_undo(request, product_id):
    next_url = request.GET.get("next")
    try:
        action_on_user = product_color_image.objects.get(id=product_id)
    except product_color_image.DoesNotExist:
        return redirect(next_url)
    action_on_user.delete_opt = True
    action_on_user.save()
    return redirect(next_url)


# ======== Color  End Delete/Undo Product  ======== #


# ========  Color (List/Unlist) Product ======== #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def product_color_list(request, product_id):
    next_url = request.GET.get("next")
    try:
        action_on_product = product_color_image.objects.get(id=product_id)
        action_on_product.status = True
        action_on_product.save()
    except products.DoesNotExist:
        return redirect(next_url)
    return redirect(next_url)


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def product_color_unlist(request, product_id):
    next_url = request.GET.get("next")
    try:
        action_on_product = product_color_image.objects.get(id=product_id)
        action_on_product.status = False
        action_on_product.save()
    except products.DoesNotExist:
        return redirect(next_url)
    return redirect(next_url)


# ========  End Color (List/Unlist) Product  ======== #

#   ========  Admin Edit Products ========   #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_edit_product(request, product_id):
    storage = messages.get_messages(request)
    storage.used = True

    next_url = request.GET.get("next")
    if request.method == "POST":
        selected_product = products.objects.get(pk=product_id)
        product_name = request.POST.get("product_name")
        product_price = request.POST.get("product_price")
        product_offer = request.POST.get("offer_percentage")
        product_description = request.POST.get("product_description")
        selected_category_id = request.POST.get("selected_category")
        if product_name:
            check_productname = views.name_test(product_name)
            if check_productname[0] is True:
                messages.error(request, check_productname[1])
                return redirect(next_url)
            selected_product.product_name = product_name
        if product_description:
            check_discription = views.description_validator(product_description)
            if check_discription[0] is True:
                messages.error(request, check_discription[1])
            selected_product.product_description = product_description
        if selected_category_id:
            selected_category = category.objects.get(pk=selected_category_id)
            selected_product.category_id = selected_category
        if product_price:
            selected_product.product_price = product_price
        if product_offer:
            check_offer = views.percentage_validator(product_offer)
            if check_offer[0] is True:
                messages.error(request, check_offer[1])
            selected_product.offer_percentage = product_offer
        selected_product.save()
        messages.success(request, f"{selected_product} updated successfully")
        return redirect("admin_product")
    context = {
        "data": products.objects.get(pk=product_id),
        "categories": category.objects.all(),
    }
    return render(request, "admin/admin_product_edit.html", context)


#   ========    END Edit Products    ========   #


#   ========  Edit Products images ========   #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def edit_product_image(request, product_id):
    storage = messages.get_messages(request)
    storage.used = True

    selected_product_color = product_color_image.objects.get(pk=product_id)
    next_url = request.GET.get("next")
    try:
        if request.method == "POST":
            product_variant_name = request.POST.get("product_variant_name")
            product_color = request.POST.get("product_color")
            image_first = request.FILES.get("image_first")
            image_second = request.FILES.get("image_second")
            image_third = request.FILES.get("image_third")
            image_fourth = request.FILES.get("image_fourth")

            if image_first is not None:
                if is_image(image_first.name):
                    selected_product_color.image_first = image_first
                else:
                    messages.error(request, "Image 1 is not a valid image")
                    return redirect(next_url)
            if image_second is not None:
                if is_image(image_second.name):
                    selected_product_color.image_second = image_second
                else:
                    messages.error(request, "Image 2 is not a valid image")
                    return redirect(next_url)
            if image_third is not None:
                if is_image(image_third.name):
                    selected_product_color.image_third = image_third
                else:
                    messages.error(request, "Image 3 is not a valid image")
                    return redirect(next_url)
            if image_fourth is not None:
                if is_image(image_fourth.name):
                    selected_product_color.image_fourth = image_fourth
                else:
                    messages.error(request, "Image 4 is not a valid image")
                    return redirect(next_url)
            if product_color is not None:
                check_color = views.color_validator(product_color)
                if check_color[0] is True:
                    messages.error(request, check_color[1])
                selected_product_color.product_color = product_color
            if product_variant_name is not None:
                if not (
                    product_variant_name[0]
                    == product_variant_name[1]
                    == product_variant_name[2]
                ):
                    (selected_product_color.product_variant_name) = product_variant_name
                else:
                    messages.error(request, "Product variant name invalid")
                    return redirect(next_url)

            selected_product_color.save()
            messages.success(request, f"{selected_product_color} updated successfully")
            return redirect(
                "admin_details_product", selected_product_color.product_id.pk
            )
    except TypeError:
        messages.error(request, "Error Occurred")

    context = {
        "selected_product_color": selected_product_color,
        "product_id": product_id,
    }
    return render(request, "admin/product_image_edit.html", context)


#   ========    END Products images    ========   #


#   ========    ADD Products  Variant  ========   #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_edit_variant(request):
    storage = messages.get_messages(request)
    storage.used = True

    product = products.objects.all()
    products_with_variant_count = products.objects.annotate(
        variant_count=Count("product_color_image")
    )
    products_with_less_than_3_variants = products_with_variant_count.filter(
        variant_count__lt=3
    )
    context = {
        "products_data": product,
        "all_varients": products_with_less_than_3_variants,
    }
    if request.method == "POST":
        product = request.POST.get("selected_product")
        product_color = request.POST.get("color")
        product_variant = request.POST.get("product_variant_name")
        thumbnail = request.FILES.get("img")
        image2 = request.FILES.get("img2")
        image3 = request.FILES.get("img3")
        image4 = request.FILES.get("img4")
        prod = products.objects.get(pk=product)
        check_variant_exist = product_color_image.objects.filter(
            product_variant_name=product_variant, product_id=prod
        ).exists()
        if check_variant_exist:
            messages.error(
                request, f"{product_variant} variant already exist of {prod}"
            )
            return redirect("admin_edit_variant")
        elif "  " in product_variant[0] or "  " in (
            product_variant[0] + product_variant[1]
        ):
            messages.error(request, "Give a valid product name")
            return redirect("admin_edit_variant")
        elif product_variant[0] == product_variant[1] == product_variant[2]:
            messages.error(request, "Give a valid product name")
            return redirect("admin_edit_variant")
        if not is_image(thumbnail.name):
            messages.error(request, "Image 1 is not a valid image")
            return redirect("admin_edit_variant")
        if not is_image(image2.name):
            messages.error(request, "Image 1 is not a valid image")
            return redirect("admin_edit_variant")
        if not is_image(image3.name):
            messages.error(request, "Image 1 is not a valid image")
            return redirect("admin_edit_variant")
        if not is_image(image4.name):
            messages.error(request, "Image 1 is not a valid image")
            return redirect("admin_edit_variant")
        check_color = views.color_validator(product_color)
        if check_color[0] is True:
            messages.error(request, check_color[1])
            return redirect("admin_edit_variant")
        data_product = product_color_image(
            product_id=prod,
            product_color=product_color,
            product_variant_name=product_variant,
            image_first=thumbnail,
            image_second=image2,
            image_third=image3,
            image_fourth=image4,
        )

        try:
            data_product.full_clean()
            data_product.save()
            messages.success(
                request, f"{product_variant} added" + " for {data_product.product_id}"
            )
        except ModuleNotFoundError:
            return redirect("admin_edit_variant")

    return render(request, "admin/admin_product_edit_varient.html", context)


#   ========    End Products  Size&Qty  ========   #

#   ========    ADD Products  Size&Qty  ========   #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_add_size_qty(request):
    storage = messages.get_messages(request)
    storage.used = True

    product_data = product_color_image.objects.annotate(
        variant_count=Count("product_size_qty")
    ).filter(variant_count__lt=4)

    if request.method == "POST":
        try:
            product_color_id = request.POST.get("select_color")
            product_quantity = int(request.POST.get("product_qty"))
            product_size = request.POST.get("product_size")
            if product_quantity < 0 or product_quantity > 10000:
                raise ValidationError()
            product_sizes_display = product_sizes_variants.objects.filter(
                product_data_id=product_color_id
            )
            product_color = product_color_image.objects.get(id=product_color_id)

            if (
                product_sizes_variants.objects.filter(
                    product_data_id=product_color
                ).count()
                < 4
            ):

                if not (
                    product_sizes_variants.objects.filter(
                        product_data_id=product_color, product_size=product_size
                    ).exists()
                ):
                    size_variant = product_sizes_variants(
                        product_data_id=product_color,
                        product_size=product_size,
                        product_quantity=int(product_quantity),
                    )

                    try:
                        size_variant.full_clean()
                        size_variant.save()
                        messages.success(request, f"Variant added for {product_color}")
                    except ValidationError as e:
                        messages.error(request, "Error ,Check the variant")
                        errors = e.message_dict

                        for field, error_messages in errors.items():
                            print(f"{field}: {', '.join(error_messages)}")
                        product_sizes_display
                        return redirect(
                            "admin_add_size_qty",
                            {"product_sizes_display": product_sizes_display},
                        )
                else:
                    messages.error(request, f"{product_size} for product exist")
        except ValueError:
            messages.error(request, "Give valid quantity")
    context = {
        "products_data": product_data,
        "sizes": ["S", "M", "L", "XL"],
    }
    return render(request, "admin/admin_add_size_qty.html", context)


#   ========    End Products  Size&Qty   ========   #


#   ========    Edit Products  Size&Qty  ========   #


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def admin_edit_size_qty(request, product_id):
    storage = messages.get_messages(request)
    storage.used = True

    next_url = request.GET.get("next")
    product_data = product_sizes_variants.objects.filter(product_data_id=product_id)
    product = product_data.first()
    context = {
        "products_data": product_data,
        "product_name": product,
        "next_url": next_url,
    }
    if request.method == "POST":
        product_quantitys = request.POST.getlist("product_qty[]")
        pro_ids = request.POST.getlist("pro[]")
        try:
            for pro_id, product_quantity in zip(pro_ids, product_quantitys):
                if product_quantity is not None:
                    if int(product_quantity) > 10000 or int(product_quantity) < 0:
                        messages.error(
                            request, "Quantity must be less than 10000, at least 0"
                        )
                        raise ValidationError()
                    product_varient = product_sizes_variants.objects.get(
                        id=pro_id, product_data_id=product_id
                    )
                    product_varient.product_quantity = product_quantity
                    product_varient.save()

        except ValidationError:
            messages.error(request, "Error Occurred,try again")
    return render(request, "admin/product_sizeqty_edit.html", context)


#   ========    End Edit  Size&Qty   ========   #


#     <<< == ==   USER  == == >>>

#   ======== All Products ========   #


def all_products_list(request):
    storage = messages.get_messages(request)
    storage.used = True

    search_query = request.POST.get("search", "")
    filter_query = request.POST.get("filter")
    page_number = request.GET.get("page")

    if search_query:
        product = product_color_image.objects.filter(
            Q(
                product_id__product_name__icontains=search_query,
                delete_opt=False,
                status=True,
                product_id__product_delete=False,
                product_id__product_list=True,
            )
            | Q(
                product_id__product_price__icontains=search_query,
                delete_opt=False,
                status=True,
                product_id__product_delete=False,
                product_id__product_list=True,
            )
        )

    elif filter_query:
        variant_name = request.POST.get("variant_name")
        color = request.POST.get("color")
        category_id = request.POST.get("category_name")
        lower_value = request.POST.get("lower_value")
        upper_value = request.POST.get("upper_value")
        filters = {
            "delete_opt": False,
            "status": True,
            "product_id__product_delete": False,
            "product_id__product_list": True,
        }
        if color:
            filters["product_color"] = color
        if category_id:
            filters["product_id__category_id"] = category_id
        if variant_name:
            filters["product_variant_name"] = variant_name
        if lower_value and upper_value:
            filters["product_id__product_price__range"] = (lower_value, upper_value)
        elif lower_value:
            filters["product_id__product_price__gte"] = lower_value
        elif upper_value:
            filters["product_id__product_price__lte"] = upper_value
        product = product_color_image.objects.filter(**filters).order_by("id")
    else:
        try:
            sort_id = request.GET.get("sort_id", None)

            sort_id = int(sort_id)
            if sort_id == 1:
                product = product_color_image.objects.filter(
                    delete_opt=False,
                    status=True,
                    product_id__product_delete=False,
                    product_id__product_list=True,
                ).order_by("-product_id__product_added_at")

            elif sort_id == 2:
                product = product_color_image.objects.filter(
                    delete_opt=False,
                    status=True,
                    product_id__product_delete=False,
                    product_id__product_list=True,
                ).order_by("-product_id__product_price")
            elif sort_id == 3:
                product = product_color_image.objects.filter(
                    delete_opt=False,
                    status=True,
                    product_id__product_delete=False,
                    product_id__product_list=True,
                ).order_by("product_id__product_price")
            elif sort_id == 4:
                product = product_color_image.objects.filter(
                    delete_opt=False,
                    status=True,
                    product_id__product_delete=False,
                    product_id__product_list=True,
                ).order_by("product_id__product_name")
            elif sort_id == 5:
                product = product_color_image.objects.filter(
                    delete_opt=False,
                    status=True,
                    product_id__product_delete=False,
                    product_id__product_list=True,
                ).order_by("-product_id__product_name")
            elif sort_id == 6:
                product = product_color_image.objects.filter(
                    delete_opt=False,
                    status=True,
                    product_id__product_delete=False,
                    product_id__product_list=True,
                    featured=True,
                ).order_by("-product_id__product_name")
            else:
                product = product_color_image.objects.filter(
                    delete_opt=False,
                    status=True,
                    product_id__product_delete=False,
                    product_id__product_list=True,
                ).order_by("-product_id__product_added_at")
        except ValueError:
            product = product_color_image.objects.filter(
                delete_opt=False,
                status=True,
                product_id__product_delete=False,
                product_id__product_list=True,
            ).order_by("product_id__product_added_at")

        except TypeError:
            product = product_color_image.objects.filter(
                delete_opt=False,
                status=True,
                product_id__product_delete=False,
                product_id__product_list=True,
            ).order_by("product_id__product_added_at")

    all_products = product_color_image.objects.all()
    variant_names = [
        product.product_variant_name
        for product in all_products
        if product.product_variant_name
    ]
    color_names = [
        product.product_color for product in all_products if product.product_color
    ]
    unique_color_names = list(set(color_names))
    unique_variant_names = list(set(variant_names))

    product = Paginator(product, 12)
    try:
        page_obj = product.get_page(page_number)
    except PageNotAnInteger:
        page_obj = product.page(1)
    except EmptyPage:
        page_obj = product.page(product.num_pages)

    context = {
        "all_products": page_obj,
        "category_data": category.objects.filter(
            is_listed=True, category_delete=True
        ).order_by("id"),
        "unique_variant_names": unique_variant_names,
        "unique_color_names": unique_color_names,
    }
    return render(request, "user/category.html", context)


# ========  End all Products  ======== #


# ========  User Products  ======== #


def user_products(request, products_id):
    storage = messages.get_messages(request)
    storage.used = True

    search_query = request.POST.get("search", "")
    filter_query = request.POST.get("filter")
    page_number = request.GET.get("page")

    if search_query:
        product = product_color_image.objects.filter(
            Q(
                product_id__product_name__icontains=search_query,
                delete_opt=False,
                status=True,
                product_id__product_delete=False,
                product_id__product_list=True,
                product_id__category_id=products_id,
            )
            | Q(
                product_id__product_price__icontains=search_query,
                delete_opt=False,
                status=True,
                product_id__product_delete=False,
                product_id__product_list=True,
                product_id__category_id=products_id,
            )
        )
    elif filter_query:
        variant_name = request.POST.get("variant_name")
        color = request.POST.get("color")
        lower_value = request.POST.get("lower_value")
        upper_value = request.POST.get("upper_value")

        filters = {
            "delete_opt": False,
            "status": True,
            "product_id__product_delete": False,
            "product_id__product_list": True,
        }
        if color:
            filters["product_color"] = color
        if variant_name:
            filters["product_variant_name"] = variant_name

        if lower_value and upper_value:
            filters["product_id__product_price__range"] = (lower_value, upper_value)
        elif lower_value:
            filters["product_id__product_price__gte"] = lower_value
        elif upper_value:
            filters["product_id__product_price__lte"] = upper_value
        product = product_color_image.objects.filter(**filters).order_by("id")
    else:
        try:
            sort_id = request.GET.get("sort_id", None)
            sort_id = int(sort_id)
            if sort_id == 1:
                product = product_color_image.objects.filter(
                    delete_opt=False,
                    status=True,
                    product_id__product_delete=False,
                    product_id__product_list=True,
                    product_id__category_id=products_id,
                ).order_by("product_id__product_added_at")
            elif sort_id == 2:
                product = product_color_image.objects.filter(
                    delete_opt=False,
                    status=True,
                    product_id__product_delete=False,
                    product_id__product_list=True,
                    product_id__category_id=products_id,
                ).order_by("-product_id__product_price")
            elif sort_id == 3:
                product = product_color_image.objects.filter(
                    delete_opt=False,
                    status=True,
                    product_id__product_delete=False,
                    product_id__product_list=True,
                    product_id__category_id=products_id,
                ).order_by("product_id__product_price")
            elif sort_id == 4:
                product = product_color_image.objects.filter(
                    delete_opt=False,
                    status=True,
                    product_id__product_delete=False,
                    product_id__product_list=True,
                    product_id__category_id=products_id,
                ).order_by("product_id__product_name")
            else:
                product = product_color_image.objects.filter(
                    delete_opt=False,
                    status=True,
                    product_id__product_delete=False,
                    product_id__product_list=True,
                    product_id__category_id=products_id,
                ).order_by("product_id__product_updated_at")
        except TypeError:
            product = product_color_image.objects.filter(
                delete_opt=False,
                status=True,
                product_id__product_delete=False,
                product_id__product_list=True,
                product_id__category_id=products_id,
            ).order_by("product_id__product_updated_at")

    all_products = product_color_image.objects.all()
    variant_names = [
        product.product_variant_name
        for product in all_products
        if product.product_variant_name
    ]
    color_names = [
        product.product_color for product in all_products if product.product_color
    ]
    unique_color_names = list(set(color_names))
    unique_variant_names = list(set(variant_names))

    product = Paginator(product, 12)
    try:
        page_obj = product.get_page(page_number)
    except PageNotAnInteger:
        page_obj = product.page(1)
    except EmptyPage:
        page_obj = product.page(product.num_pages)

    context = {
        "selected_category": category.objects.get(id=products_id),
        "category_products": page_obj,
        "product_id": products_id,
        "category_data": category.objects.filter(
            is_listed=True, category_delete=True
        ).order_by("id"),
        "unique_variant_names": unique_variant_names,
        "unique_color_names": unique_color_names,
    }

    return render(request, "user/product_page.html", context)


# ======== Products Details  ======== #


def product_details(request, products_id):
    storage = messages.get_messages(request)
    storage.used = True

    product_data = product_color_image.objects.filter(pk=products_id)
    context = {
        "category_data": category.objects.filter(is_listed=True).order_by("id"),
        "product_data": product_data,
    }

    return render(request, "user/product_detailsss.html", context)


# ======== End Details  ======== #
