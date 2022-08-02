from django import template
from django.db.models import Q

from ..models import Page

register = template.Library()


@register.inclusion_tag("tailwind/super_featured_objects.html")
def super_featured_page_list(objects):
    """super_featured_page_list Every Super Featured Pages for links lists"""
    objects = Page.objects.filter(featuring_state="SF")
    return {"objects": objects}


@register.inclusion_tag("tailwind/featured.html")
def all_featured_pages():
    """A list of all the featured pages"""
    objects = Page.objects.filter(~Q(featuring_state="N")).order_by("-featuring_state")[:7]
    return {"objects": objects}
