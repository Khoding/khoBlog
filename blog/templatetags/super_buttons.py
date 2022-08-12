from django import template
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

register = template.Library()


@register.inclusion_tag("tailwind/super_buttons.html")
def sb(o, *args, **kwargs):
    """Superbutton tag"""
    user = kwargs.get("user")
    liked = False
    authenticated = False
    admin = False
    if user and user.is_authenticated:
        authenticated = True
        if hasattr(o, "likes"):
            liked = user in o.likes.all()
    if user and user.is_superuser and not user.secure_mode is True:
        authenticated = True
        admin = True
    return {"object": o, "admin": admin, "authenticated": authenticated, "liked": liked}


@register.inclusion_tag("tailwind/user_super_buttons.html")
def usb(o):
    """User superbutton tag"""
    return {"object": o}


@register.inclusion_tag("tailwind/content_super_buttons.html")
def csb(o):
    """Content superbutton tag"""
    content_type = ContentType.objects.get_for_model(o)
    create_url = reverse(f"{content_type.app_label}:create_{content_type.model}")
    obj = o.__class__.__name__
    return {"object": obj, "create_url": create_url}


@register.inclusion_tag("tailwind/user_auth_button.html")
def user_auth_sb(o):
    """User auth button tag"""
    return {
        "object": o,
    }
