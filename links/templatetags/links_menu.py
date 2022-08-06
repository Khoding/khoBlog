from django import template

from links.models import Links

register = template.Library()


@register.inclusion_tag("tailwind/links_list.html")
def links_menu():
    """Links menu tag"""
    urls = Links.objects.filter(shown=True).order_by("priority")
    return {"urls": urls}


@register.filter
def add_slash_to_slug(slug):
    """Adds a slash to the end of a slug"""
    return "/" + slug
