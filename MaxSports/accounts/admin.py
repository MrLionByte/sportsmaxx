from django.contrib import admin
from accounts.models import Image, user_address, referral


# Import models classes


# Register your models here.


admin.site.register(user_address)
admin.site.register(Image)
admin.site.register(referral)
