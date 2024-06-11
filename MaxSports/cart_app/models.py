from django.db import models
from django.contrib.auth.models import User
from product_app.models import product_sizes_variants, product_color_image
from coupons_app.models import Coupons

# Create your models here.


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    product_color_variant = models.ForeignKey(
        product_color_image, on_delete=models.SET_NULL, null=True
    )

    def __str__(self) -> str:
        return f"{self.product_color_variant} on {self.added_on}"


class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total_amount_without_coupon = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coupon = models.ForeignKey(
        Coupons, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    coupon_active = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"'{self.user_id}'s cart"

    def remove_coupon(self):
        self.coupon = None
        self.coupon_active = False
        self.save()


class Cart_products(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    product_color_variant = models.ForeignKey(
        product_sizes_variants, on_delete=models.SET_NULL, null=True
    )
    quantity = models.PositiveIntegerField(default=1)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{Cart} = {self.product_color_variant}"


class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    coupon = models.ForeignKey(
        Coupons, on_delete=models.SET_NULL, null=True, default=None
    )
    coupon_active = models.BooleanField(default=False, null=True)
    sub_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, null=True
    )

    def __str__(self):
        return f" {self.cart} Checkout"
