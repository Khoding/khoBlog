from django import template
from settings_app.models import UserArea

register = template.Library()


@register.inclusion_tag('settings_app/users_area_setting.html')
def setting(users):
    users = UserArea.objects.filter(users_area__shown=True)
    return {'users': users}
