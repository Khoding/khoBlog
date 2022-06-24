from django import template

register = template.Library()


@register.inclusion_tag('tailwind/status_dot.html')
def status_dot(o):
    """Returns status dot"""
    return {'object': o}
