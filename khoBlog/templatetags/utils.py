import random

from django import template

register = template.Library()


@register.simple_tag
def random_int(a, b=None):
    """Returns a random integer"""
    if b is None:
        a, b = 0, a
    return random.randint(a, b)


@register.filter(name="prefix")
def prefix(value, prefix=""):
    """Prefixes a string"""
    if value != "":
        return f"{prefix}{value}"
    return ""


@register.filter(name="suffix")
def suffix(value, suffix=""):
    """Suffixes a string"""
    if value != "":
        return f"{value}{suffix}"
    return ""
