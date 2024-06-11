from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class Coupons(models.Model):
    title = models.CharField(max_length=30, blank=True)
    code = models.CharField(max_length=20, unique=True, default="xxxx")
    valid_from = models.DateField(null=True, blank=True)
    expiry = models.DateField(null=True, blank=True)
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    discount_percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True
    )
    max_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    min_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=False, null=True)
    created_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title
