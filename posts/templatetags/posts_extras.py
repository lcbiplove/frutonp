from django import template
from posts.models import Post
register = template.Library()

@register.filter
def get_from_negative(value):
    last = None

    last = value[-1]

    return last

@register.filter
def subtract(value, arg):
    return value - arg

""" Get food choices from the value """
@register.filter
def get_display_food_choice(value):
    return dict(Post.FOOD_CHOICES).get(value, value)

""" Get quantity choice from the value """
@register.filter
def get_display_quantity_choice(value):
    return dict(Post.QUANTITY_CHOICES).get(value, value)