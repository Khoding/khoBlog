from django.contrib import admin

from .models import MenuFooter, MenuFooterLink


class MenuFooterLinksInline(admin.TabularInline):
    model = MenuFooterLink
    extra = 0


class MenuFooterAdmin(admin.ModelAdmin):
    inlines = [
        MenuFooterLinksInline,
    ]


admin.site.register(MenuFooter, MenuFooterAdmin)
