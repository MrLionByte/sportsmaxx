from django.contrib import admin
from .models import products, product_color_image, product_sizes_variants

# Register your models here.

admin.site.register(products)
admin.site.register(product_sizes_variants)
admin.site.register(product_color_image)
