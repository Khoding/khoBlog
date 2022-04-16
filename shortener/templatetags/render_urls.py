from django import template

from shortener.models import URL

register = template.Library()


@register.inclusion_tag("tailwind/links_list.html")
def links_n(urls):
    urls = URL.objects.filter(featured=True)
    return {"urls": urls}
