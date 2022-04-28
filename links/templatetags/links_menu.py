from django import template

from links.models import Links

register = template.Library()


@register.inclusion_tag("tailwind/links_list.html")
def links_menu(urls, mobile=False):
    if mobile is True:
        mobile = True
    urls = Links.objects.filter(shown=True).order_by("priority")
    return {"urls": urls, "mobile": mobile}


@register.filter
def add_slash_to_slug(slug):
    return "/" + slug
