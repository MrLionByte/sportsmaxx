# Generated by Django 5.0.4 on 2024-06-03 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("banner_app", "0002_main_banner_added_at_sub_banner_added_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="main_banner",
            name="expiry",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="main_banner",
            name="start",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="main_banner",
            name="status",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="sub_banner",
            name="expiry",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="sub_banner",
            name="start",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="sub_banner",
            name="status",
            field=models.BooleanField(default=True),
        ),
    ]
