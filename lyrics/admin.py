from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Song


# quote admin
@admin.register(Song)
class SongAdmin(SimpleHistoryAdmin):
    """Song Admin Class"""

    list_display = (
        "pk",
        "title",
    )
    list_display_links = ("title",)
    ordering = ("pk",)

    # prepopulate slug field with person name title property
    prepopulated_fields = {"slug": ("title",)}
