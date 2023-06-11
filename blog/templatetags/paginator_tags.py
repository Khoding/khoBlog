from django import template
from django.core.paginator import Paginator

register = template.Library()


@register.simple_tag
def get_proper_elided_page_range(p, number, on_each_side=3, on_ends=2):
    """Paginator get_proper_elided_page_range override"""
    paginator = Paginator(p.object_list, p.per_page, p.orphans)
    return paginator.get_elided_page_range(number=number, on_each_side=on_each_side, on_ends=on_ends)


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    """relative_url tag"""
    url = f"?{field_name}={value}"

    if urlencode:
        querystring = urlencode.split("&")
        filtered_querystring = filter(lambda p: p.split("=")[0] != field_name, querystring)
        encoded_querystring = "&".join(filtered_querystring)
        url = f"{url}"
        if encoded_querystring:
            url = f"{url}&{encoded_querystring}"
    return url
