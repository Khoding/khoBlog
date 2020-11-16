from django.contrib import admin

from .models import URL


class URLAdmin(admin.ModelAdmin):
    list_display = ('title', 'full_url', 'slug', 'clicks', 'featured',)
    ordering = ('-pk',)
    search_fields = ('title', 'slug', 'pk', 'full_url')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(URL, URLAdmin)
