from django import template

register = template.Library()


@register.filter(name="remove_duplicates")
def remove_duplicates(lst):
    return list(set(lst))
