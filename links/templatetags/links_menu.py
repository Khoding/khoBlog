from django import template

from links.models import Links

register = template.Library()


@register.inclusion_tag("tailwind/links_list.html")
def links_menu(urls, device):
    """Links menu tag"""
    dev_class = True
    urls = Links.objects.filter(shown=True).order_by("priority")
    if device == "desktop":
        dev_class = False
    return {"urls": urls, "dev_class": dev_class}


@register.filter
def add_slash_to_slug(slug):
    """Adds a slash to the end of a slug"""
    return "/" + slug
