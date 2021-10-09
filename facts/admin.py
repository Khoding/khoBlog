from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Fact


class FactAdmin(SimpleHistoryAdmin):
    """FactAdmin
    Admin for Facts
    """

    prepopulated_fields = {
        "slug": ("title",),
    }


admin.site.register(Fact, FactAdmin)
