from django import template

register = template.Library()


@register.inclusion_tag("blog/base_post_card.html", takes_context=True)
def render_cards(context, o, in_list=False):
    return {
        "context": context,
        "object": o,
        "in_list": in_list,
    }
