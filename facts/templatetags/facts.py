from django import template

register = template.Library()
from facts.models import Fact


@register.inclusion_tag("facts/fact_display.html")
def fact(hide_header=False, hide_readmore=False):
    """fact inclusion tag"""
    facts = Fact.objects.filter(shown=True)
    if facts.count() > 0:
        o = facts.order_by("?")[0]
        return {
            "object": o,
            "hide_header": hide_header,
            "hide_readmore": hide_readmore,
        }
