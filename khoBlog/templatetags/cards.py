from django import template

register = template.Library()


@register.inclusion_tag("tailwind/cards.html", takes_context=True)
def cards(context, o, in_list=False):
    """Card tag"""
    return {
        "context": context,
        "object": o,
        "in_list": in_list,
    }
