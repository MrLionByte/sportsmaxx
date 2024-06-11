# myapp/context_processors.py
from category_app.models import category


def custom_context(request):
    category_data = category.objects.filter(is_listed=True).order_by("category_name")
    return {
        "category_data": category_data,
    }
