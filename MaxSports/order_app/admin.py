from django.contrib import admin
from .models import Order, Order_items, Cancelled_order

# Register your models here.

admin.site.register(Order)
admin.site.register(Order_items)
admin.site.register(Cancelled_order)
