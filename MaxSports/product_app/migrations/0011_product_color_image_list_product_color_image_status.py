# Generated by Django 5.0.4 on 2024-04-27 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product_app", "0010_alter_product_sizes_variants_product_data_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="product_color_image",
            name="list",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="product_color_image",
            name="status",
            field=models.BooleanField(default=True),
        ),
    ]
