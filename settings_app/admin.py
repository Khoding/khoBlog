from django.contrib import admin

from .models import (
    Footer,
    LinksFooter,
    LinksGroupSideMenu,
    LinksSideMenu,
    MenuFooter,
    MenuFooterLink,
    Settings,
    SideMenu,
    SpecificDateMessage,
)


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "area_visible",
    )


class PresetsSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "shown",
    )


class LinksSideMenuInline(admin.TabularInline):
    model = LinksSideMenu
    extra = 0


class LinksGroupSideMenuAdmin(admin.ModelAdmin):
    list_display = ("title",)

    inlines = [
        LinksSideMenuInline,
    ]


class SpecificDateMessageMenuInline(admin.TabularInline):
    model = SpecificDateMessage
    extra = 0


class SideMenuAdmin(admin.ModelAdmin):
    inlines = [
        SpecificDateMessageMenuInline,
    ]


class LinksFooterInline(admin.TabularInline):
    model = LinksFooter
    extra = 0


class FooterAdmin(admin.ModelAdmin):
    inlines = [
        LinksFooterInline,
    ]


class MenuFooterLinksInline(admin.TabularInline):
    model = MenuFooterLink
    extra = 0


class MenuFooterAdmin(admin.ModelAdmin):
    inlines = [
        MenuFooterLinksInline,
    ]


admin.site.register(SideMenu, SideMenuAdmin)
admin.site.register(Footer, FooterAdmin)
admin.site.register(MenuFooter, MenuFooterAdmin)
admin.site.register(LinksGroupSideMenu, LinksGroupSideMenuAdmin)
admin.site.register(Settings, PresetsSettingsAdmin)
