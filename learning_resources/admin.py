from django.contrib import admin
from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'done',)
    list_editable = ('done',)
    list_filter = ('done',)
