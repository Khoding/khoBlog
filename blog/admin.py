from django.contrib import admin, messages
from django.core import serializers
from django.http import HttpResponse
from django.utils.translation import ngettext
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Category, Post, PostCatsLink, Series


class PostResource(resources.ModelResource):
    """Admin class for PostResource"""

    class Meta:
        """Meta class for PostResource"""

        model = Post


def export_as_json(queryset):
    """Export a queryset as JSON"""
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


def make_published(modeladmin, request, queryset):
    """Make a queryset of posts published"""
    updated = queryset.update(publication_state="P")
    modeladmin.message_user(
        request,
        ngettext(
            "%d post was successfully marked as published.",
            "%d posts were successfully marked as published.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


def make_withdrawn(modeladmin, request, queryset):
    """Make a queryset of posts withdrawn"""
    updated = queryset.update(publication_state="W")
    modeladmin.message_user(
        request,
        ngettext(
            "%d post was successfully marked as withdrawn.",
            "%d posts were successfully marked as withdrawn.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


def make_featured(modeladmin, request, queryset):
    """Make a queryset of posts featured"""
    updated = queryset.update(featuring_state="F")
    modeladmin.message_user(
        request,
        ngettext(
            "%d post was successfully marked as featured.",
            "%d posts were successfully marked as featured.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


def make_super_featured(modeladmin, request, queryset):
    """Make a queryset of posts super featured"""
    updated = queryset.update(featuring_state="SF")
    modeladmin.message_user(
        request,
        ngettext(
            "%d post was successfully marked as super featured.",
            "%d posts were successfully marked as super featured.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


def make_not_featuredd(modeladmin, request, queryset):
    """Make a queryset of posts not featured"""
    updated = queryset.update(featuring_state="N")
    modeladmin.message_user(
        request,
        ngettext(
            "%d post was successfully marked as not featured.",
            "%d posts were successfully marked as not featured.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


def make_baguette(modeladmin, request, queryset):
    """Make a queryset of posts baguette"""
    updated = queryset.update(language="FR")
    modeladmin.message_user(
        request,
        ngettext(
            "%d post was successfully marked as Language Baguette.",
            "%d posts were successfully marked as Language Baguette.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


def make_english(modeladmin, request, queryset):
    """Make a queryset of posts English"""
    updated = queryset.update(language="EN")
    modeladmin.message_user(
        request,
        ngettext(
            "%d post was successfully marked as Language English.",
            "%d posts were successfully marked as Language English.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


def make_other_language(modeladmin, request, queryset):
    """Make a queryset of posts other language"""
    updated = queryset.update(language="OL")
    modeladmin.message_user(
        request,
        ngettext(
            "%d post was successfully marked as Another Language.",
            "%d posts were successfully marked as Another Language.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


def make_multi_lingui(modeladmin, request, queryset):
    """Make a queryset of posts multi lingual"""
    updated = queryset.update(language="ML")
    modeladmin.message_user(
        request,
        ngettext(
            "%d post was successfully marked as Multi Linguistic.",
            "%d posts were successfully marked as Multi Linguistic.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


class PostCatsLinkInline(admin.TabularInline):
    """PostCatsLinkInline Class"""

    model = PostCatsLink
    extra = 0


class PostAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    """PostAdmin Class"""

    resource_class = PostResource
    list_display = (
        "pk",
        "title",
        "created_date",
        "pub_date",
        "slug",
        "vanity_url",
        "publication_state",
        "featuring_state",
        "featured_cat_title",
        "clicks",
        "rnd_choice",
        "language",
        "deleted_at",
    )
    list_display_links = (
        "pk",
        "title",
    )
    ordering = (
        "-pk",
        "title",
        "-pub_date",
        "-deleted_at",
    )
    search_fields = (
        "title",
        "featured_title",
        "slug",
        "pk",
        "withdrawn",
        "featuring_state",
        "url_to_article",
        "url_to_article_title",
    )
    prepopulated_fields = {
        "slug": ("title",),
    }
    list_filter = (
        "deleted_at",
        "needs_reviewing",
        "publication_state",
        "featuring_state",
        "pub_date",
        "withdrawn",
        "featuring_state",
        "categories",
        "language",
        "tags",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "featured_title",
                    "description",
                    "author",
                    "slug",
                    "vanity_url",
                    "body",
                    "tags",
                )
            },
        ),
        (
            ("States"),
            {
                "fields": (
                    "withdrawn",
                    "deleted_at",
                    "publication_state",
                    "featuring_state",
                    "language",
                    "needs_reviewing",
                    "enable_comments",
                )
            },
        ),
        (
            ("Post Type"),
            {
                "fields": (
                    "image",
                    "url_to_article",
                    "url_to_article_title",
                )
            },
        ),
        (
            ("Dates"),
            {
                "fields": (
                    "created_date",
                    "pub_date",
                )
            },
        ),
    )

    inlines = [PostCatsLinkInline]

    actions = [
        make_published,
        make_withdrawn,
        make_featured,
        make_super_featured,
        make_not_featuredd,
        export_as_json,
        make_baguette,
        make_english,
        make_other_language,
        make_multi_lingui,
    ]


class CategoryAdmin(SimpleHistoryAdmin):
    """CategoryAdmin Class"""

    list_display = ("title", "suffix", "description", "slug", "withdrawn", "deleted_at")
    ordering = (
        "-pk",
        "title",
        "-deleted_at",
    )
    search_fields = ("title", "slug", "pk", "withdrawn")
    prepopulated_fields = {
        "slug": (
            "title",
            "suffix",
        )
    }
    list_filter = (
        "withdrawn",
        "deleted_at",
        "parent",
    )


@admin.register(Series)
class SeriesAdmin(SimpleHistoryAdmin):
    """SeriesAdmin Class"""

    list_display = ("title", "description", "slug", "withdrawn", "deleted_at")
    ordering = (
        "-pk",
        "title",
        "-deleted_at",
    )
    search_fields = ("title", "slug", "pk", "withdrawn")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = (
        "withdrawn",
        "deleted_at",
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
