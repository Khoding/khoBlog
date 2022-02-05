from django import template

register = template.Library()


@register.simple_tag()
def o_count(o):
    return o.model.objects.only("pk").filter(is_removed=False).count()
