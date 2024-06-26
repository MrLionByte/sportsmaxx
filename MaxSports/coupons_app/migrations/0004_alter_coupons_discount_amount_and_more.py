# Generated by Django 5.0.4 on 2024-05-15 16:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coupons_app", "0003_alter_coupons_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coupons",
            name="discount_amount",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="coupons",
            name="discount_percentage",
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
            ),
        ),
    ]
