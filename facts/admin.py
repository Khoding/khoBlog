from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Fact, SpecificDateFact


class FactAdmin(SimpleHistoryAdmin):
    """FactAdmin
    Admin for Facts
    """

    prepopulated_fields = {
        "slug": ("title",),
    }


class SpecificDateFactAdmin(SimpleHistoryAdmin):
    """SpecificDateFactAdmin
    Admin for SpecificDateFacts
    """

    prepopulated_fields = {
        "slug": ("title",),
    }


admin.site.register(Fact, FactAdmin)
admin.site.register(SpecificDateFact, SpecificDateFactAdmin)
