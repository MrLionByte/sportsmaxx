from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import random
import string
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class user_address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    delete_address = models.BooleanField(default=False, blank=False)
    full_name = models.CharField(max_length=50, blank=False, default="to add")
    landmark = models.CharField(max_length=30, blank=True, null=True)
    address_type = models.CharField(
        max_length=10, default="Home", blank=False, null=False
    )
    accessible = models.CharField(max_length=50, default="Not Added", blank=False)
    area = models.CharField(max_length=50, default="Not Added", blank=False)
    city = models.CharField(max_length=50, default="Not Added", blank=False)
    pincode_regex = RegexValidator(
        regex=r"^\d{6}$", message="Pincode must be 6 'digits'"
    )
    pincode = models.CharField(max_length=6, validators=[pincode_regex])
    post_office = models.CharField(
        max_length=40, null=False, blank=False, default="Not Added"
    )
    state = models.CharField(
        max_length=40, null=False, blank=False, default="Not Added"
    )
    phone_regex = RegexValidator(
        regex=r"^\d{10}$", message="Phone number must be 10 'digits'"
    )
    phone_no = models.CharField(
        max_length=10, validators=[phone_regex], default="00000000"
    )
    alternative_phone = models.CharField(
        max_length=10, validators=[phone_regex], blank=True
    )

    def __str__(self) -> str:
        return self.user.username


class Image(models.Model):
    image = models.ImageField(upload_to="images/")

    def __str__(self) -> str:
        return str(self.pk)


class referral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    referral_code = models.CharField(max_length=160, unique=True)

    def __str__(self) -> str:
        return self.referral_code


def generate_referral_code(username):
    random_number = "".join(random.choices(string.digits, k=5))
    return f"{username}{random_number}"


@receiver(post_save, sender=User)
def create_referral(sender, instance, created, **kwargs):
    if created:
        referral_code = generate_referral_code(instance.username)
        while referral.objects.filter(referral_code=referral_code).exists():
            referral_code = generate_referral_code(instance.username)
        referral.objects.create(user=instance, referral_code=referral_code)
