from custom_taggit.models import CustomTag, CustomTaggedItem
from django.contrib import admin

# Register your models here.


class CustomTaggedItemAdmin(admin.StackedInline):
    model = CustomTaggedItem
    extra = 0


@admin.register(CustomTag)
class CustomTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'withdrawn',)

    inlines = [CustomTaggedItemAdmin, ]
