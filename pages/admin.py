from django.contrib import admin
from .models import FlatPage
from django.contrib.flatpages.models import FlatPage as FlatPageOld


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'modified_date', 'slug')
    ordering = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('sites', 'registration_required')

    fieldsets = (
        (None, {'fields': ('title', 'page_head',
                           'content', 'description', 'modified_date', 'sites', 'slug',)}),
        (('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('registration_required', 'template_name'),
        }),
    )


admin.site.unregister(FlatPageOld)
admin.site.register(FlatPage, PageAdmin)
