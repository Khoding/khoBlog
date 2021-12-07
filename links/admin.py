from django.contrib import admin

from .models import Links


class LinksAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "priority", "permalink", "slug", "shown")
    ordering = ("-pk",)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Links, LinksAdmin)
