from django import template

register = template.Library()

@register.filter
def get_from_negative(value):
    last = None

    last = value[-1]

    return last

@register.filter
def subtract(value, arg):
    return value - arg