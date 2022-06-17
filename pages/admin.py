from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Page


@admin.register(Page)
class PageAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    """Admin class for Page"""

    list_display = ("title", "created_date", "slug", "deleted_at")
    ordering = ("title",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    list_filter = (
        "sites",
        "registration_required",
        "deleted_at",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "page_head",
                    "content",
                    "description",
                    "sites",
                    "created_date",
                    "slug",
                )
            },
        ),
        (
            ("Advanced options"),
            {
                "classes": ("collapse",),
                "fields": ("registration_required", "template_name"),
            },
        ),
    )
