from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Song, Artist, Genre


@admin.register(Song)
class SongAdmin(SimpleHistoryAdmin):
    """Song Admin Class"""

    list_display = (
        "pk",
        "title",
    )
    list_display_links = ("title",)
    ordering = ("pk",)

    prepopulated_fields = {"slug": ("title",)}


@admin.register(Artist)
class ArtistAdmin(SimpleHistoryAdmin):
    """Artist Admin Class"""

    list_display = (
        "pk",
        "name",
    )
    list_display_links = ("name",)
    ordering = ("pk",)

    prepopulated_fields = {"slug": ("name",)}


@admin.register(Genre)
class GenreAdmin(SimpleHistoryAdmin):
    """Genre Admin Class"""

    list_display = (
        "pk",
        "title",
    )
    list_display_links = ("title",)
    ordering = ("pk",)

    prepopulated_fields = {"slug": ("title",)}
