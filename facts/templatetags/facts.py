from datetime import datetime
from random import randrange

from django import template
from django.db.models import Q

register = template.Library()
from facts.models import Fact, SpecificDateFact


@register.inclusion_tag("facts/fact_display.html", takes_context=True)
def fact(context, hide_header=False, hide_readmore=False):
    """fact inclusion tag"""
    facts = Fact.objects.filter(shown=True)
    if facts.count() > 0:
        o = facts.order_by("?")[0]
        return {
            "object": o,
            "hide_header": hide_header,
            "hide_readmore": hide_readmore,
            "context": context,
        }


@register.inclusion_tag("facts/specific_date_fact_display.html", takes_context=True)
def specific_date_fact(context, hide_header=False, hide_readmore=False):
    """specific_date_fact inclusion tag"""
    facts = SpecificDateFact.objects.filter(
        (
            Q(
                showing_date__day=datetime.today().day,
                showing_date__month=datetime.today().month,
                showing_rule="D",
            )
            | Q(showing_date__hour=datetime.now().hour, showing_rule="T")
            | Q(
                showing_date__day=datetime.today().day,
                showing_date__month=datetime.today().month,
                showing_date__hour=datetime.now().hour,
                showing_rule="DT",
            )
        )
        & (Q(is_recurrent=True) | Q(is_recurrent=False, showing_date__year=datetime.now().year))
    )
    if facts.count() > 0:
        o = facts.order_by("?")[0]
        return {
            "object": o,
            "hide_header": hide_header,
            "hide_readmore": hide_readmore,
            "context": context,
        }


@register.inclusion_tag("facts/facts.html", takes_context=True)
def facts(context):
    """fax bruh"""
    rnd = randrange(2)
    return {"rnd": rnd, "context": context}
