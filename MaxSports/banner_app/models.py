from django.db import models
from product_app.models import product_color_image

# Create your models here.


class main_banner(models.Model):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(
        product_color_image, on_delete=models.SET_NULL, null=True
    )
    description = models.TextField(blank=True)
    added_at = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)
    expiry = models.DateField(null=True, blank=True)
    start = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class sub_banner(models.Model):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(
        product_color_image, on_delete=models.SET_NULL, null=True
    )
    added_at = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)
    expiry = models.DateField(null=True, blank=True)
    start = models.DateField(null=True, blank=True)
