from django import template

from ..models import Page

register = template.Library()


@register.inclusion_tag("tailwind/super_featured_objects.html")
def super_featured_page_list():
    """super_featured_page_list Every Super Featured Pages for links lists"""
    objects = Page.objects.filter(featuring_state="SF")
    return {"objects": objects}


@register.inclusion_tag("tailwind/featured_objects.html")
def featured_page_list():
    """featured_post_list Every Featured Pages for links lists"""
    objects = Page.objects.filter(featuring_state="F")
    return {"objects": objects}
