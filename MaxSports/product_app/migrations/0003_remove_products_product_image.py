# Generated by Django 5.0.4 on 2024-04-20 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product_app", "0002_product_color_image_image_fourth"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="products",
            name="product_image",
        ),
    ]
