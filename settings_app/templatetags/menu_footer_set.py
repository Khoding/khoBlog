from django import template
from django.contrib.auth import get_user_model

from settings_app.models import MenuFooterLink

register = template.Library()
User = get_user_model()


@register.inclusion_tag("tailwind/menu_footer_links.html", takes_context=True)
def mfl_setting(context, menu_footer_links, device, link_type):
    has_perms = context.get("perms", ["settings_app.view_menu_footer_link"])
    dev_class = True
    if link_type == "D":
        menu_footer_links = MenuFooterLink.objects.filter(visibility="D")
    if context.request.user.is_authenticated:
        if link_type == "NP" and has_perms:
            menu_footer_links = MenuFooterLink.objects.filter(visibility="NP")
        elif link_type == "NS" and context.request.user.is_staff:
            menu_footer_links = MenuFooterLink.objects.filter(visibility="NS")
        elif link_type == "NA" and context.request.user.is_superuser:
            menu_footer_links = MenuFooterLink.objects.filter(visibility="NA")
    if device == "desktop":
        dev_class = False
    return {"context": context, "menu_footer_links": menu_footer_links, "dev_class": dev_class}
