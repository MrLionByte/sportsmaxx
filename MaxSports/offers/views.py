from django.shortcuts import render, redirect
from django.http import JsonResponse
from category_app.models import category
from product_app.models import products
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from all_validator import views

# Create your views here.


# <===== CATEGORy OFFERS =====>


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def category_offers(request):
    storage = messages.get_messages(request)
    storage.used = True

    context = {
        "cat_all": True,
        "category_for_offer": category.objects.all().order_by("-offer_percentage"),
    }
    return render(request, "admin/admin_offer_cat.html", context)


# <===== END CATEGORy OFFERS =====>


# <===== EDIT CATEGORy OFFERS =====>


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def edit_category_offers(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == "POST":
        category_id = request.POST.get("categoryId")
        offer_percentage = request.POST.get("offerPercentage")
        try:
            check_percentage = views.percentage_validator(offer_percentage)
            if check_percentage[0] is True:
                messages.error(request, check_percentage[1])
                return redirect("category_offers")
            cat = category.objects.get(pk=category_id)
            cat.offer_percentage = offer_percentage
            cat.save()
            return JsonResponse({"success": True})
        except category.DoesNotExist:
            return JsonResponse({"success": False, "error": "Category not found"})
    else:
        return JsonResponse({"success": False, "error": "Invalid request"})


# <===== END EDIT CATEGORy OFFERS =====>


# <===== Product OFFERS =====>


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def product_offers(request):
    storage = messages.get_messages(request)
    storage.used = True

    context = {
        "product_for_offer": products.objects.all().order_by("-offer_percentage"),
    }
    return render(request, "admin/admin_offer_pro.html", context)


# <===== End Product OFFERS =====>

# <===== Product OFFERS =====>


@user_passes_test(lambda u: u.is_superuser, login_url="/admin_login/")
def edit_product_offers(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == "POST":
        product_id = request.POST.get("productId")
        offer_percentage = request.POST.get("offerPercentage")
        try:
            check_offer = views.percentage_validator(offer_percentage)
            if check_offer[0] is True:
                messages.error(request, check_offer[1])
                return JsonResponse({"success": False})
            else:
                product = products.objects.get(pk=product_id)
                product.offer_percentage = offer_percentage
                product.save()
                return JsonResponse(
                    {"success": True, "new_offer_percentage": product.offer_percentage}
                )
        except product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product not found"})
    else:
        return JsonResponse({"success": False, "error": "Invalid request"})


# <===== End Product OFFERS =====>]
