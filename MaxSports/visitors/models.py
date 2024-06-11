from django.db import models
from django.utils import timezone
from django.db.models import Count
import datetime


class Visitor(models.Model):
    ip_address = models.CharField(max_length=40)
    visit_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Visitor from {self.ip_address} on {self.visit_time}"

    @classmethod
    def today_vs_month_percentage(cls):
        now = timezone.now()
        today_start = timezone.make_aware(
            datetime.datetime.combine(now.date(), datetime.time.min)
        )
        today_end = timezone.make_aware(
            datetime.datetime.combine(now.date(), datetime.time.max)
        )

        today_visitors = cls.objects.filter(
            visit_time__range=(today_start, today_end)
        ).count()

        month_start = timezone.make_aware(
            datetime.datetime.combine(now.replace(day=1).date(), datetime.time.min)
        )
        month_to_today_visitors = cls.objects.filter(
            visit_time__range=(month_start, today_end)
        ).count()

        if month_to_today_visitors == 0:
            return 0
        percentage = (today_visitors / month_to_today_visitors) * 100
        return percentage
