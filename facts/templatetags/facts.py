from datetime import datetime

from django import template
from django.db.models import Q

from facts.models import SpecificDateFact

register = template.Library()


@register.inclusion_tag("tailwind/display_fact.html")
def facts():
    """Facts tag"""
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
    if specific_date_fact_count != 0:
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
            o.rnd_chosen()
            is_old_enough = False
            timesince = datetime.now().year - o.showing_date.year
            if timesince > 0:
                is_old_enough = True
            return {
                "object": o,
                "is_old_enough": is_old_enough,
                "timesince": timesince,
            }
    else:
        return None
