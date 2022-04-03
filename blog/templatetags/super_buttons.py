from django import template

register = template.Library()


@register.inclusion_tag("blog/includes/super_buttons.html")
def sb(o):
    return {"object": o}


@register.inclusion_tag("tailwind/super_buttons.html")
def twsb(o):
    return {"object": o}


@register.inclusion_tag("tailwind/user_super_buttons.html")
def twusb(o):
    return {"object": o}
