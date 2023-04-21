from django import template

register = template.Library()


@register.filter()
def decorate_text(value):
    return value.capitalize()
