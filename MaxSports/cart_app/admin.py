from django.contrib import admin
from .models import Cart, Checkout, Cart_products

# Register your models here.

admin.site.register(Cart)
admin.site.register(Cart_products)
admin.site.register(Checkout)
