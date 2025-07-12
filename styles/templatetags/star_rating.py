from django import template

register = template.Library()

@register.simple_tag
def render_stars(rating, max_stars=5):
    try:
        rating = float(rating)
    except (ValueError, TypeError):
        rating = 0

    filled = '★' * int(rating)
    empty = '☆' * (max_stars - int(rating))
    return filled + empty
