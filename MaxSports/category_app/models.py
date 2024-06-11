from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class category(models.Model):
    category_name = models.CharField(
        max_length=100, unique=True, null=False, blank=False
    )
    category_image = models.ImageField(upload_to="category/", blank=True)
    created_at = models.DateField(auto_now_add=True, auto_now=False)
    updated_at = models.DateField(auto_now=True, auto_now_add=False)
    is_listed = models.BooleanField(default=True)
    types_available = models.CharField(blank=False, max_length=20, default="Other")
    offer_percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], default=0
    )
    category_delete = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return self.category_name


class available_types(models.Model):
    type = models.CharField(max_length=20)
    created_on = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.type
