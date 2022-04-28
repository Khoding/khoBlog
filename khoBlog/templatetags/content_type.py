from django import template

register = template.Library()


@register.filter
def to_class_name(value, lower=True):
    val = value.__class__.__name__
    if lower is True:
        val = val.lower()
    return val
