from django.contrib import admin, messages
from django.utils.translation import ngettext

from taggit.models import Tag

from custom_taggit.models import CustomTag, CustomTaggedItem


def make_default_color(modeladmin, request, queryset):
    """Make a queryset of tags default color"""
    updated = queryset.update(color="#9B8383")
    modeladmin.message_user(
        request,
        ngettext(
            "%d tag was attributed default color.",
            "%d tags were attributed default color.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


class CustomTaggedItemAdmin(admin.StackedInline):
    """Admin class for CustomTaggedItem"""

    model = CustomTaggedItem
    extra = 0


@admin.register(CustomTag)
class CustomTagAdmin(admin.ModelAdmin):
    """Admin class for CustomTag"""

    list_display = (
        "name",
        "slug",
        "withdrawn",
        "color",
    )

    list_filter = (
        "withdrawn",
        "color",
    )

    inlines = [
        CustomTaggedItemAdmin,
    ]

    actions = [
        make_default_color,
    ]


admin.site.unregister(Tag)
