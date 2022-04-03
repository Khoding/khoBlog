from django.template import Library

register = Library()


@register.inclusion_tag("tailwind/theme_buttons.html")
def theme_button(position):
    container = False
    if position == "darkLightd":
        container = True
    return {"position": position, "container": container}
