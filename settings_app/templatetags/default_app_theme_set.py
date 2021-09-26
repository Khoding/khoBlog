from django import template

from settings_app.models import Settings

register = template.Library()


@register.inclusion_tag("settings_app/default_app_theme_setting.html")
def dt_setting(themes):
    themes = Settings.objects.filter(shown=True)
    return {"themes": themes}


@register.inclusion_tag("settings_app/all_themes.html")
def all_theme_setting(themes):
    themes = Settings.THEME_CHOICES
    return {"themes": themes}
