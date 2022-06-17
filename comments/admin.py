from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django_comments_xtd.admin import XtdCommentsAdmin

from .models import CustomCommentXTD


def make_site_khoblog(modeladmin, request, queryset):
    """Changes the site of a queryset of comments to khoblog"""
    updated = queryset.update(site_id=1)
    modeladmin.message_user(
        request,
        ngettext(
            "%d comment was successfully added to site khoblog.",
            "%d comments were successfully added to site khoblog.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


def make_site_localhost(modeladmin, request, queryset):
    """Changes the site of a queryset of comments to localhost"""
    updated = queryset.update(site_id=2)
    modeladmin.message_user(
        request,
        ngettext(
            "%d comment was successfully added to site localhost.",
            "%d comments were successfully added to site localhost.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


class CommentsXTDAdmin(XtdCommentsAdmin):
    """Admin class for CommentsXTD"""

    list_display = (
        "cid",
        "thread_level",
        "nested_count",
        "name",
        "content_type",
        "object_pk",
        "ip_address",
        "submit_date",
        "followup",
        "is_public",
        "is_removed",
    )
    list_display_links = ("cid",)
    list_filter = ("content_type", "is_public", "is_removed", "followup")
    fieldsets = (
        (None, {"fields": ("content_type", "object_pk", "site")}),
        (
            "Content",
            {
                "fields": (
                    "title",
                    "user",
                    "user_name",
                    "user_email",
                    "user_url",
                    "comment",
                    "followup",
                )
            },
        ),
        (
            "Metadata",
            {"fields": ("submit_date", "ip_address", "is_public", "is_removed")},
        ),
    )
    date_hierarchy = "submit_date"
    ordering = ("thread_id", "order")
    search_fields = [
        "object_pk",
        "user__username",
        "user_name",
        "user_email",
        "comment",
    ]

    list_filter = (
        "submit_date",
        "site",
        "is_public",
        "is_removed",
    )

    actions = [
        "flag_comments",
        "approve_comments",
        "remove_comments",
        make_site_khoblog,
        make_site_localhost,
    ]


admin.site.register(CustomCommentXTD, CommentsXTDAdmin)
