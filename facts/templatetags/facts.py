from django import template

register = template.Library()
from facts.models import Fact


@register.inclusion_tag("facts/fact_display.html")
def fact():
    """fact inclusion tag"""
    facts = Fact.objects.filter(shown=True)
    if facts.count() > 0:
        o = facts.order_by("?")[0]
        return {"object": o}
