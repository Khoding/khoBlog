from django import template
from links.models import Links

register = template.Library()


@register.inclusion_tag('links/links_list.html')
def links_menu(urls):
    urls = Links.objects.filter(shown=True).order_by('priority')
    return {'urls': urls}
