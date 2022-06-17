from django.contrib import admin

from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """Admin class for Resource"""

    list_display = (
        "title",
        "url",
        "done",
        "withdrawn",
    )
    list_editable = ("done",)
    list_filter = (
        "done",
        "withdrawn",
    )
