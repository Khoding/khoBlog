from django import template


register = template.Library()


# inclusion tag for mega menu
@register.inclusion_tag("tailwind/mega_menu.html", takes_context=True)
def mega_menu(context, menu):
    """Mega menu tag"""
    return {"user": context.request.user, "menu": menu}


# inclusion tag for menu tab
@register.inclusion_tag("tailwind/menu_sections_mobile.html", takes_context=True)
def tab_menu(context, menu):
    """Tab menu tag"""
    return {"user": context.request.user, "menu": menu}
