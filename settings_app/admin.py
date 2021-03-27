from django.contrib import admin
from .models import LinksFooter, LinksGroupSideMenu, SideMenu, LinksSideMenu, Settings, Footer


class UsersAdmin(admin.ModelAdmin):
    list_display = ('title', 'area_visible',)


class PresetsSettingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'shown',)


class LinksGroupSideMenuAdmin(admin.ModelAdmin):
    list_display = ('title',)


class LinksSideMenuInline(admin.TabularInline):
    model = LinksSideMenu
    extra = 0


class SideMenuAdmin(admin.ModelAdmin):
    inlines = [LinksSideMenuInline, ]


class LinksFooterInline(admin.TabularInline):
    model = LinksFooter
    extra = 0


class FooterAdmin(admin.ModelAdmin):
    inlines = [LinksFooterInline, ]


admin.site.register(SideMenu, SideMenuAdmin)
admin.site.register(Footer, FooterAdmin)
admin.site.register(LinksGroupSideMenu, LinksGroupSideMenuAdmin)
admin.site.register(Settings, PresetsSettingsAdmin)
