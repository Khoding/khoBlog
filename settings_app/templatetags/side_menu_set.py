from django import template
from settings_app.models import SideMenu

register = template.Library()


@register.inclusion_tag('settings_app/side_menu_setting.html', takes_context=True)
def setting(context, sides):
    sides = SideMenu.objects.filter(side_menus__shown=True)
    return {'sides': sides, 'context': context}
