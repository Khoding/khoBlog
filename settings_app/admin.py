from django.contrib import admin

from .models import MenuFooter, MenuFooterLink


class MenuFooterLinksInline(admin.TabularInline):
    """Inline class for MenuFooterLink"""

    model = MenuFooterLink
    extra = 0


class MenuFooterAdmin(admin.ModelAdmin):
    """Admin class for MenuFooter"""

    inlines = [
        MenuFooterLinksInline,
    ]


admin.site.register(MenuFooter, MenuFooterAdmin)
