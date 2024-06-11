from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db import transaction


# Create your models here.


class Wallet_User(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user_id}, {self.amount}, {self.balance}"


class Wallet_transactions(models.Model):
    wallet_id = models.ForeignKey(Wallet_User, on_delete=models.SET_NULL, null=True)
    # transaction_id = models.CharField(max_length=70, default='000000')
    transaction_for = models.CharField(max_length=50, default=None)
    date_of_transaction = models.DateField(auto_now_add=True)
    amount_sent = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True
    )
    amount_received = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True
    )
    delete = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.transaction_for

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Wallet_transactions.objects.get(pk=self.pk)
            old_amount_sent = old_instance.amount_sent or 0
            old_amount_received = old_instance.amount_received or 0

            if self.wallet_id:
                with transaction.atomic():
                    self.wallet_id.balance += old_amount_sent
                    self.wallet_id.balance -= old_amount_received
                    self.wallet_id.amount += old_amount_sent + old_amount_received
                    self.wallet_id.save()

        super().save(*args, **kwargs)

        if self.wallet_id:
            with transaction.atomic():
                if self.amount_sent:
                    self.wallet_id.balance -= self.amount_sent
                    self.wallet_id.amount += self.amount_sent
                if self.amount_received:
                    self.wallet_id.balance += self.amount_received
                    self.wallet_id.amount += self.amount_received
                self.wallet_id.save()
