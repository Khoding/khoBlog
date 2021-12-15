from django import template

register = template.Library()


@register.inclusion_tag("blog/base_post_card.html", takes_context=True)
def render_cards(context, o, is_featured=False, in_list=False):
    return {
        "context": context,
        "object": o,
        "is_featured": is_featured,
        "in_list": in_list,
    }
