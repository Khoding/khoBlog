from django.utils import timezone
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def o_count(context, o):
    if context.request.user.is_superuser:
        return o.model.objects.only("pk").filter(is_removed=False).count()
    else:
        return (
            o.model.objects.only("pk").filter(pub_date__lte=timezone.now(), withdrawn=False, is_removed=False).count()
        )
