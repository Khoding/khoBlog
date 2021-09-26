from datetime import datetime

from django import template
from django.db.models import Q

from settings_app.models import SpecificDateMessage

register = template.Library()


@register.inclusion_tag(
    "settings_app/specific_date_message_setting.html", takes_context=True
)
def specific_date_message_setting(context, messages):
    messages = SpecificDateMessage.objects.filter(
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
        & (
            Q(is_recurrent=True)
            | Q(is_recurrent=False, showing_date__year=datetime.now().year)
        )
    )
    return {"messages": messages, "context": context}
