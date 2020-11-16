from django import template
from shortener.models import URL

register = template.Library()


@register.inclusion_tag('shortener/links_list.html')
def links(urls):
    urls = URL.objects.filter(quick=True)
    return {'urls': urls}
