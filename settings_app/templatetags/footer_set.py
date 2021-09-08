from django import template

from settings_app.models import Footer

register = template.Library()


@register.inclusion_tag('settings_app/footer_setting.html', takes_context=True)
def footer_setting(context, footers):
    footers = Footer.objects.filter(footers__shown=True)
    return {'footers': footers, 'context': context}
