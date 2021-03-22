from django.contrib import admin
from .models import LinksGroupSideMenu, UserArea, SideMenu, LinksSideMenu, Settings


class UsersAdmin(admin.ModelAdmin):
    list_display = ('title', 'area_visible',)


class PresetsSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'shown',)


class LinksGroupSideMenuAdmin(admin.ModelAdmin):
    list_display = ('name',)


class LinksSideMenuInline(admin.TabularInline):
    model = LinksSideMenu
    extra = 0


class SideMenuAdmin(admin.ModelAdmin):
    inlines = [LinksSideMenuInline, ]


admin.site.register(UserArea, UsersAdmin)
admin.site.register(SideMenu, SideMenuAdmin)
admin.site.register(LinksGroupSideMenu, LinksGroupSideMenuAdmin)
admin.site.register(Settings, PresetsSettingsAdmin)
