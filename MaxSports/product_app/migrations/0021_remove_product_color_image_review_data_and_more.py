# Generated by Django 5.0.4 on 2024-06-02 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product_app", "0020_product_color_image_review_data_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product_color_image",
            name="review_data",
        ),
        migrations.RemoveField(
            model_name="product_color_image",
            name="review_star",
        ),
    ]
