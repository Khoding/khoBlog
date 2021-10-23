from datetime import datetime
from random import randrange

from django import template
from django.db.models import Q

register = template.Library()
from facts.models import Fact, SpecificDateFact


@register.inclusion_tag("facts/facts.html", takes_context=True)
def facts(context, hide_header=False, hide_readmore=False):
    """fax bruh"""
    rnd = randrange(2)
    specific_date_fact_count = SpecificDateFact.objects.filter(
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
    ).count()
    if rnd == 0 or specific_date_fact_count == 0:
        facts = Fact.objects.filter(shown=True)
        if facts.count() > 0:
            o = facts.order_by("?")[0]
            return {
                "object": o,
                "hide_header": hide_header,
                "hide_readmore": hide_readmore,
                "simple_fact": True,
                "context": context,
            }
    elif rnd == 1 and specific_date_fact_count != 0:
        facts = SpecificDateFact.objects.filter(shown=True).filter(
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
            is_old_enough = False
            timesince = datetime.now().year - o.showing_date.year
            if timesince > 0:
                is_old_enough = True
            return {
                "object": o,
                "hide_header": hide_header,
                "hide_readmore": hide_readmore,
                "simple_fact": False,
                "is_old_enough": is_old_enough,
                "timesince": timesince,
                "context": context,
            }
