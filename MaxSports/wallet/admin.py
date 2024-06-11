from django.contrib import admin
from .models import Wallet_transactions, Wallet_User

# Register your models here.

admin.site.register(Wallet_transactions)
admin.site.register(Wallet_User)
