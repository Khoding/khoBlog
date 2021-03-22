from django import template
from settings_app.models import AboutArea

register = template.Library()


@register.inclusion_tag('settings_app/about_area_setting.html')
def setting(abouts):
    abouts = AboutArea.objects.filter(about_area__shown=True)
    return {'abouts': abouts}
