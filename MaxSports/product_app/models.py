from django.db import models
from category_app.models import category
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class products(models.Model):
    category_id = models.ForeignKey(category, null=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=70, null=False, blank=False, unique=True)
    product_description = models.TextField(blank=True)
    product_price = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    offer_percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], default=0
    )
    product_added_at = models.DateField(auto_now=True)
    product_updated_at = models.DateField(auto_now_add=True)
    product_delete = models.BooleanField(blank=False, default=False)
    product_list = models.BooleanField(blank=False, default=False)

    def __str__(self) -> str:
        return self.product_name

    def category_check(self) -> str:
        return self.category_id.category_name

    def product_price_after(self):
        if int(self.offer_percentage) >= (int(self.category_id.offer_percentage)):
            product_offer = self.product_price - (
                self.offer_percentage * self.product_price / 100
            )
        else:
            product_offer = self.product_price - (
                self.category_id.offer_percentage * self.product_price / 100
            )
        return round(product_offer)


class product_color_image(models.Model):
    product_id = models.ForeignKey(products, on_delete=models.CASCADE, default=None)
    product_color = models.CharField(blank=False, null=False, max_length=30)
    product_variant_name = models.CharField(blank=True, null=True, max_length=30)
    image_first = models.ImageField(upload_to="product/", blank=False)
    image_second = models.ImageField(upload_to="product/", blank=False)
    image_third = models.ImageField(upload_to="product/", blank=False)
    image_fourth = models.ImageField(
        upload_to="product/", blank=False, default="img coming"
    )
    delete_opt = models.BooleanField(blank=False, default=False)
    status = models.BooleanField(blank=False, default=True)
    featured = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return f"{self.product_id.product_name} ({self.product_color})"

    def to_show(self):
        return f"{self.product_id.product_name}  >> {self.product_color}"


class product_sizes_variants(models.Model):
    product_data_id = models.ForeignKey(
        product_color_image,
        related_name="product_size_qty",
        on_delete=models.CASCADE,
        default=0,
    )
    product_quantity = models.IntegerField(
        default=0, validators=[MaxValueValidator(10000)]
    )
    product_size = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.product_size} of {self.product_data_id}"
