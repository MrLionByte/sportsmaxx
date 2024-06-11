# Generated by Django 5.0.4 on 2024-04-20 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="available_types",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=20)),
                ("created_on", models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category_name", models.CharField(max_length=100, unique=True)),
                (
                    "category_image",
                    models.ImageField(blank=True, upload_to="category/"),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                ("is_listed", models.BooleanField(default=True)),
                ("category_delete", models.BooleanField(default=False)),
                (
                    "types_available",
                    models.ManyToManyField(to="category_app.available_types"),
                ),
            ],
        ),
    ]