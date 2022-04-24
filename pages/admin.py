from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Page


@admin.register(Page)
class PageAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    list_display = ("title", "created_date", "slug", "is_removed")
    list_editable = ("is_removed",)
    ordering = ("title",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    list_filter = (
        "sites",
        "registration_required",
        "is_removed",
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
