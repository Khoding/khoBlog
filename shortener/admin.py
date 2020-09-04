from django.contrib import admin

from .models import URL


class URLAdmin(admin.ModelAdmin):

    prepopulated_fields = {'short_url': ('name',)}


admin.site.register(URL, URLAdmin)
