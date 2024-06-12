from django.db import models
from django.contrib.auth.models import User
from product_app.models import product_color_image

# from coupons_app.models import Coupons
from accounts.models import user_address
from django.utils import timezone


# Create your models here.


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    serial_number = models.AutoField(primary_key=True, unique=True, editable=False)
    address = models.ForeignKey(
        user_address, on_delete=models.SET_NULL, null=True, blank=True
    )
    payment_method = models.CharField(max_length=20)
    payment_online_id = models.CharField(
        max_length=50, default="0000", null=True, blank=True
    )
    order_date = models.DateTimeField(auto_now_add=True)
    coupon_name = models.CharField(max_length=50, null=True, blank=True)
    coupon_discount = models.CharField(max_length=50, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_to_pay = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            max_serial_number = Order.objects.aggregate(models.Max("serial_number"))[
                "serial_number__max"
            ]
            if max_serial_number is not None:
                self.serial_number = max_serial_number + 1
            else:
                self.serial_number = 100001
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.serial_number}"


class Order_items(models.Model):
    STATUS_CHOICES = (
        ("Order Pending", "Order Pending"),
        ("Order confirmed", "Order confirmed"),
        ("Shipped", "Shipped"),
        ("Out For Delivery", "Out For Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
        ("Returned", "Returned"),
    )
    order = models.ForeignKey(
        Order, related_name="order_all", on_delete=models.CASCADE, null=True, blank=True
    )
    product_added = models.ForeignKey(
        product_color_image, on_delete=models.SET_NULL, null=True, blank=True
    )
    quantity = models.IntegerField(default=00)
    size = models.CharField(max_length=20, default="toadd")
    last_update = models.DateTimeField(auto_now=True)
    final_product_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=False, default=0.00
    )
    status = models.CharField(choices=STATUS_CHOICES, default="Order Pending")
    cancel_return_confirm = models.BooleanField(default=False)
    accept_order = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.order} ,PK{self.pk}"

    def expected_delivery_date(self):
        self.expected_date = self.order.order_date + timezone.timedelta(days=10)
        return self.expected_date


class Cancelled_order(models.Model):
    ordered_item = models.ForeignKey(Order_items, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reason = models.TextField(null=True, blank=True)
    request_date = models.DateField(auto_now_add=True, null=True)
    pickup_date = models.DateField(null=True, blank=True)
    has_dispatched = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self) -> str:
        s = f" Order_id = {self.ordered_item.pk}"
        x = f", return status = {self.ordered_item.status}"
        return s + x
