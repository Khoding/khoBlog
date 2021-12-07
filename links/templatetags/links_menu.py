from django import template

from links.models import Link

register = template.Library()


@register.inclusion_tag("links/links_list.html", takes_context=True)
def links_menu(context, urls):
    urls = Link.objects.filter(shown=True).order_by("priority")
    return {"urls": urls, "context": context}


@register.filter
def add_slash_to_slug(slug):
    return "/" + slug
