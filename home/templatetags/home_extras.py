from django import template
from posts.models import Post

register = template.Library()

""" Get food choices from the value """
@register.filter
def get_display_food_choice(value):
    return dict(Post.FOOD_CHOICES).get(value)