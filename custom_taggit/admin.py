from django.contrib import admin
from taggit.models import Tag

from custom_taggit.models import CustomTag, CustomTaggedItem


class CustomTaggedItemAdmin(admin.StackedInline):
    model = CustomTaggedItem
    extra = 0


@admin.register(CustomTag)
class CustomTagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "withdrawn",
    )

    inlines = [
        CustomTaggedItemAdmin,
    ]


admin.site.unregister(Tag)
