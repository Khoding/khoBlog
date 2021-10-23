from django import template
from django.core.paginator import Paginator

register = template.Library()


@register.simple_tag
def get_proper_elided_page_range(p, number, on_each_side=3, on_ends=2):
    """Paginator get_proper_elided_page_range override"""
    paginator = Paginator(p.object_list, p.per_page, p.orphans)
    return paginator.get_elided_page_range(number=number, on_each_side=on_each_side, on_ends=on_ends)
