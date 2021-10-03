from django import template

register = template.Library()


@register.inclusion_tag("blog/includes/post_offcanvas.html")
def offcanvas(o):
    return {"object": o}
