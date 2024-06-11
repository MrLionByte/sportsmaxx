# Generated by Django 5.0.4 on 2024-05-17 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart_app", "0007_cart_coupon"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="total_amount_without_coupon",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]