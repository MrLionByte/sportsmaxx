# Generated by Django 5.0.4 on 2024-05-17 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product_app", "0016_alter_products_product_delete"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="product_name",
            field=models.CharField(max_length=70, unique=True),
        ),
    ]