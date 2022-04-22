from django import template
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

register = template.Library()


@register.inclusion_tag("tailwind/super_buttons.html")
def sb(o):
    return {"object": o}


@register.inclusion_tag("tailwind/user_super_buttons.html")
def usb(o):
    return {"object": o}


@register.inclusion_tag("tailwind/content_super_buttons.html")
def csb(o):
    content_type = ContentType.objects.get_for_model(o)
    create_url = reverse("%s:create_%s" % (content_type.app_label, content_type.model))
    obj = o.__class__.__name__
    return {"object": obj, "create_url": create_url}
