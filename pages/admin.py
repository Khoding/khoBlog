from django.contrib import admin
from .models import Page


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'update_date', 'slug')
    ordering = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Page, PageAdmin)
