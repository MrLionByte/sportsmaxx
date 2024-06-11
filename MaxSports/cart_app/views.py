from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from product_app.models import product_sizes_variants, product_color_image
from accounts.models import user_address
from .models import Cart, Cart_products, Wishlist, Coupons
from wallet.models import Wallet_User, Wallet_transactions
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from category_app.models import category
from django.http import JsonResponse
import json
from django.db.models import Count
from django.utils import timezone
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from order_app.models import Order
from django.db.models import Q, Subquery
from django.views.decorators.cache import never_cache

# Create your views here.
date_now = (timezone.now()).date()


# ======    SHOW CART     ====== #


@never_cache
@login_required
def cart_show(request):
    storage = messages.get_messages(request)
    storage.used = True

    user = request.user
    try:
        user_cart = Cart.objects.get(user_id=user)
    except Cart.DoesNotExist:
        cart = Cart(user_id=user)
        cart.save()
        user_cart = Cart.objects.get(user_id=user)
    cart_total = user_cart.total_amount

    available_coupons = Coupons.objects.filter(
        min_limit__lte=cart_total,
        max_limit__gte=cart_total,
        expiry__gte=date_now,
        valid_from__lte=date_now,
        is_active=True,
    )

    cart_all = Cart_products.objects.filter(cart=user_cart).order_by("-id")
    for product in cart_all:
        if (
            not product.product_color_variant.product_data_id.status
            or product.product_color_variant.product_data_id.delete_opt
        ):
            product.delete()
            messages.info(
                request,
                f"Sorry, {product.product_color_variant.
                                             product_data_id} is currently unavailable to buy",
            )
        if product.product_color_variant.product_quantity == 0:
            product.delete()
            messages.info(
                request,
                f"Sorry, {product.product_color_variant.
                                             product_data_id} is currently unavailable to buy",
            )

    cart_all = Cart_products.objects.filter(cart=user_cart).order_by("-id")
    context = {
        "user_cart": user_cart,
        "cart_all": cart_all,
        "category_data": category.objects.filter(is_listed=True),
        "available_coupons": available_coupons,
    }
    if user_cart:
        return render(request, "user/cart.html", context)
    else:
        return redirect("home")


# ======  END SHOW CART  ====== #


# ====== ADD PRODUCT CART ====== #


@login_required
def add_product_to_cart(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == "POST":
        user_in_action = User.objects.get(username=request.user)
        product_id_to_add = request.POST.get("product_id")
        product_size = request.POST.get("product_size")
        redirect_wishlist = request.POST.get("redirect_wishlist")

        try:
            user_selected_product = product_sizes_variants.objects.get(
                product_data_id=product_id_to_add, product_size=product_size
            )

        except ObjectDoesNotExist:
            user_selected_product = product_sizes_variants.objects.get(
                id=product_id_to_add
            )
        if not Cart.objects.filter(user_id=request.user).exists():
            new_cart = Cart()
            new_cart.user_id = user_in_action
            new_cart.save()

        user_cart = Cart.objects.get(user_id=user_in_action)
        cart_products_count = Cart_products.objects.filter(cart=user_cart).aggregate(
            num_items=Count("id")
        )["num_items"]

        if Cart_products.objects.filter(
            product_color_variant=user_selected_product, cart=user_cart
        ):
            messages.error(request, "Product already added to the cart")
            if redirect_wishlist is not None:
                return redirect("show_wishlist")
            return redirect("product_details", product_id_to_add)
        elif cart_products_count > 9:
            messages.error(
                request,
                "Cart is overloaded,Finish the purchase" + " or remove few products",
            )
            if redirect_wishlist is not None:
                return redirect("show_wishlist")
            return redirect("product_details", product_id_to_add)
        price = user_selected_product.product_data_id.product_id.product_price_after()
        Cart_products.objects.get_or_create(
            cart=user_cart,
            product_color_variant=user_selected_product,
            sub_total=float(price),
        )
        user_cart.total_amount = user_cart.total_amount + Decimal(price)
        user_cart.total_amount_without_coupon = user_cart.total_amount
        user_cart.save()
        messages.success(request, f"{user_selected_product} added to cart")
        if redirect_wishlist is not None:
            return redirect("show_wishlist")
        return redirect("product_details", product_id_to_add)


# ====== END ADD PRODUCT ====== #


# ======    REMOVE CART     ====== #


@login_required
def remove_from_cart(request):
    storage = messages.get_messages(request)
    storage.used = True

    try:
        delete_id = request.GET.get("delete_id", None)
        cart_product = Cart_products.objects.get(id=delete_id)
        users_cart = Cart.objects.get(user_id=request.user)
        users_cart.total_amount = users_cart.total_amount - cart_product.sub_total
        users_cart.total_amount_without_coupon = users_cart.total_amount
        users_cart.save()
        cart_product.delete()
        return redirect("cart_show")
    except Cart.DoesNotExist:
        messages.error(request, "Couldn't delete cart item")
        return redirect("cart_show")


# ======  END REMOVE CART  ====== #


# ====== UPDATE TOTAL PRICE  ====== #


@login_required
def update_total_price(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == "POST":
        data = json.loads(request.body)
        quantity = data.get("quantity")
        product_id = data.get("productId")
        user = request.user
        cart = Cart.objects.get(user_id=user)
        cart_added_item = Cart_products.objects.get(id=product_id, cart=cart)

        if int(quantity) > 10:
            messages.error(request, "Maximum quantity10 is allowed")
            return redirect("cart_show")
        elif int(quantity) > (cart_added_item.product_color_variant.product_quantity):
            price = (
                cart_added_item.product_color_variant.product_data_id.product_id.product_price_after()
            )
            total_price = quantity * price

            cart_added_item.quantity = quantity
            cart_added_item.sub_total = total_price
            cart_added_item.save()
            return JsonResponse(
                {
                    "stockError": True,
                    "message": "Sorry, only "
                    + str(cart_added_item.product_color_variant.product_quantity)
                    + " left in stock",
                    "availableQuantity": cart_added_item.product_color_variant.product_quantity,
                }
            )
        elif (
            not cart_added_item.product_color_variant.product_data_id.status
            or cart_added_item.product_color_variant.product_data_id.delete_opt
        ):
            cart_added_item.delete()
            messages.error(
                request,
                f"Sorry, only {cart_added_item.product_color_variant.product_data_id}",
            )
            return redirect("cart_show")
        price = (
            cart_added_item.product_color_variant.product_data_id.product_id.product_price_after()
        )
        total_price = quantity * price

        cart_added_item.quantity = quantity
        cart_added_item.sub_total = total_price
        cart_added_item.save()

        all_cart_items = Cart_products.objects.filter(cart=cart)
        if all_cart_items:
            total_amount_final = 0.00
            for cart_item in all_cart_items:
                product_price = (
                    cart_item.product_color_variant.product_data_id.product_id.product_price_after()
                )
                quantity = cart_item.quantity
                sub_total = product_price * quantity
                total_amount_final += sub_total
        else:
            total_amount_final = 0.00
        if total_amount_final < 4999:
            total_amount_final = total_amount_final + 150

        cart.total_amount = total_amount_final
        cart.total_amount_without_coupon = total_amount_final
        cart.save()

        return JsonResponse(
            {
                "success": True,
                "totalPrice": total_price,
                "subTotal": str(total_amount_final),
            }
        )

    return redirect("cart_show")


# ====== END UPDATE TOTAL PRICE ====== #


# ======  APPLY COUPON  ====== #
@login_required
def apply_coupon(request):
    storage = messages.get_messages(request)
    storage.used = True

    coupon_code = request.GET.get("coupon", None)
    user = request.user
    user_cart = Cart.objects.get(user_id=user)
    coupon_obj = Coupons.objects.get(code=coupon_code)
    if Order.objects.filter(user_id=user, coupon_name=coupon_obj).exists():
        messages.info(request, "You already used it, Not available")
        return redirect("cart_show")
    if not coupon_obj.min_limit <= user_cart.total_amount:
        messages.info(request, "Cannot apply coupon")
        return redirect("cart_show")
    elif not coupon_obj.max_limit > user_cart.total_amount:
        messages.info(request, "Cannot apply coupon")
        return redirect("cart_show")
    if Cart.objects.filter(user_id=request.user, coupon=coupon_obj).exists():
        messages.info(request, "Already added the coupon")
        return redirect("cart_show")
    if user_cart.total_amount != user_cart.total_amount_without_coupon:
        user_cart.total_amount = user_cart.total_amount_without_coupon
        user_cart.save()

    try:
        coupon_id = Coupons.objects.get(code=coupon_code)
        if coupon_id.discount_amount:
            coupon_discount = coupon_id.discount_amount
            amount_after_coupon = user_cart.total_amount - coupon_discount
        else:
            coupon_discount = coupon_id.discount_percentage
            amount_after_coupon = user_cart.total_amount - (
                coupon_discount * user_cart.total_amount / 100
            )

        user_cart.total_amount = amount_after_coupon
        user_cart.coupon = coupon_id
        user_cart.coupon_active = True
        user_cart.save()
        return redirect("cart_show")
    except Cart.DoesNotExist:
        return redirect("cart_show")


# ====== END APPLY COUPON ====== #


# ====== DELETE COUPON ====== #
@login_required
def delete_coupon(request):
    user_cart = Cart.objects.get(user_id=request.user)
    user_cart.total_amount = user_cart.total_amount_without_coupon
    user_cart.remove_coupon()
    user_cart.save()
    messages.success(request, "Coupon removed successfully")
    return redirect("cart_show")


# ====== END COUPON ====== #


#  << ====== CHECKOUT  ====== >>

# ====== ADD CHECKOUT PRODUCT ====== #

# ====== END CHECKOUT PRODUCT ====== #


# ======    CHECKOUT PRODUCT     ====== #
@never_cache
@login_required
def checkout_product(request):
    storage = messages.get_messages(request)
    storage.used = True

    try:
        user = request.user
        user_addresses = user_address.objects.filter(
            user_id=user, delete_address=False
        ).order_by("-id")

        cart = Cart.objects.get(user_id=user)
        users_cart = Cart_products.objects.filter(cart=cart)
        if not users_cart:
            messages.info(request, "Add products in cart first !!")
            return redirect("cart_show")
        final_sum = cart.total_amount
        coupon = cart.coupon
        try:
            if cart.coupon.discount_amount:
                coupon_discount = cart.coupon.discount_amount
            else:
                coupon_discount = cart.coupon.discount_percentage
        except AttributeError:
            coupon_discount = None
        context = {
            "user_addresses": user_addresses,
            "cart_all": users_cart,
            "total_sum": final_sum,
            "final_sum": final_sum,
            "coupon": coupon,
            "coupon_discount": coupon_discount,
            "wallet": Wallet_User.objects.get(user_id=request.user),
        }
    except Cart.DoesNotExist:
        return redirect("cart_show")
    return render(request, "user/checkout.html", context)


# ======    END CHECKOUT     ====== #

#  << ====== Wishlist  ====== >>


# ======    SHOW WISHLIST     ====== #


@login_required
@never_cache
def show_wishlist(request):
    storage = messages.get_messages(request)
    storage.used = True

    users_wishlist = Wishlist.objects.filter(user=request.user)
    size_variants = []
    for wishlist_item in users_wishlist:
        product_color_variant = wishlist_item.product_color_variant
        size = product_sizes_variants.objects.filter(
            product_data_id=product_color_variant
        )
        size_variants.extend(size)
    context = {
        "all_wishlist": users_wishlist,
        "size_variants": size_variants,
    }
    return render(request, "user/wishlist.html", context)


# ====== END SHOW WISHLIST ====== #


# ======     ADD TO WISHLIST    ====== #


@login_required
def add_to_wishlist(request, product_id):
    storage = messages.get_messages(request)
    storage.used = True

    next_url = request.GET.get("next")
    product = product_color_image.objects.get(id=product_id)

    if not Wishlist.objects.filter(
        user=request.user, product_color_variant=product
    ).exists():
        Wishlist.objects.get_or_create(user=request.user, product_color_variant=product)
        messages.success(request, "Product added to wishlist" + "successfully")
        return redirect(next_url)
    else:
        messages.error(request, "Product already exists in your wishlist.")
        return redirect(next_url)


# ====== END ADD TO WISHLIST ====== #


# ====== END ADD TO WISHLIST ====== #


@login_required
def delete_from_wishlist(request):
    storage = messages.get_messages(request)
    storage.used = True

    try:
        delete_id = request.GET.get("delete_id", None)
        cart_product = Wishlist.objects.get(id=delete_id)
        cart_product.delete()
        return redirect("show_wishlist")
    except Wishlist.DoesNotExist:
        messages.error(request, "Couldn't delete cart item")
        return redirect("show_wishlist")


# ====== END ADD TO WISHLIST ====== #
