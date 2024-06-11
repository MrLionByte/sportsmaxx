from django.shortcuts import get_object_or_404
from .models import Visitor
from django.utils import timezone


class VisitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract IP address (consider using a proxy server for reliability)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(",")[0]
        else:
            ip_address = request.META.get("REMOTE_ADDR")

        # Create a new Visitor record if one doesn't exist within a reasonable timeframe (e.g., 15 minutes)
        visitor, created = Visitor.objects.get_or_create(
            ip_address=ip_address, defaults={"visit_time": timezone.now()}
        )

        if created:
            # New visitor detected, optionally log or perform actions
            pass

        response = self.get_response(request)
        return response
