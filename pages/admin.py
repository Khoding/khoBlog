from django.contrib import admin
from .models import FlatPage
from django.contrib.flatpages.models import FlatPage as FlatPageOld


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'slug')
    ordering = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('sites', 'registration_required')

    fieldsets = (
        (None, {'fields': ('title', 'page_head',
                           'content', 'description', 'sites', 'created_date',  'slug',)}),
        (('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('registration_required', 'template_name'),
        }),
    )


admin.site.unregister(FlatPageOld)
admin.site.register(FlatPage, PageAdmin)
