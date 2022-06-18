from django.contrib import admin, messages
from django.utils.translation import ngettext

from simple_history.admin import SimpleHistoryAdmin

from .models import Fact, SpecificDateFact


def make_shown(modeladmin, request, queryset):
    """Changes the visibility of a queryset of facts to shown"""
    updated = queryset.update(shown=True)
    modeladmin.message_user(
        request,
        ngettext(
            "%d fact was successfully marked as shown.",
            "%d facts were successfully marked as shown.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


def make_hidden(modeladmin, request, queryset):
    """Changes the visibility of a queryset of facts to hidden"""
    updated = queryset.update(shown=False)
    modeladmin.message_user(
        request,
        ngettext(
            "%d fact was successfully marked as hidden.",
            "%d facts were successfully marked as hidden.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


class FactAdmin(SimpleHistoryAdmin):
    """FactAdmin
    Admin for Facts
    """

    prepopulated_fields = {
        "slug": ("title",),
    }

    actions = [
        make_shown,
        make_hidden,
    ]


class SpecificDateFactAdmin(SimpleHistoryAdmin):
    """SpecificDateFactAdmin
    Admin for SpecificDateFacts
    """

    prepopulated_fields = {
        "slug": ("title",),
    }

    actions = [
        make_shown,
        make_hidden,
    ]


admin.site.register(Fact, FactAdmin)
admin.site.register(SpecificDateFact, SpecificDateFactAdmin)
