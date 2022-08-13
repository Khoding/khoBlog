from django import template

from settings_app.models import MenuFooterLink

register = template.Library()


@register.inclusion_tag("tailwind/menu_footer_links.html", takes_context=True)
def mfl_setting(context, link_type):
    """Menu footer links tag"""
    has_perms = context.get("perms", ["settings_app.view_menu_footer_link"])
    menu_footer_links = ""
    if link_type == "D":
        menu_footer_links = MenuFooterLink.objects.filter(visibility="D")
    if context.request.user.is_authenticated:
        if link_type == "NP" and has_perms:
            menu_footer_links = MenuFooterLink.objects.filter(visibility="NP")
        elif link_type == "NS" and context.request.user.is_staff:
            menu_footer_links = MenuFooterLink.objects.filter(visibility="NS")
        elif link_type == "NA" and context.request.user.is_superuser:
            menu_footer_links = MenuFooterLink.objects.filter(visibility="NA")
        elif link_type == "NAL" and context.request.user.is_superuser:
            menu_footer_links = MenuFooterLink.objects.filter(visibility="NAL")
    return {"menu_footer_links": menu_footer_links}
