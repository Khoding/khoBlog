import random
from django import template

register = template.Library()


@register.simple_tag
def random_int(a, b=None):
    if b is None:
        a, b = 0, a
    return random.randint(a, b)


@register.filter(name='prefix')
def prefix(value, prefix=''):
    if value != '':
        return f'{prefix}{value}'
    return ''


@register.filter(name='suffix')
def suffix(value, suffix=''):
    if value != '':
        return f'{value}{suffix}'
    return ''
