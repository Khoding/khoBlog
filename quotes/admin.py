from django.contrib import admin

# register quotes models
from quotes.models import Category, MediaType, Person, Quote, Source


# quote admin
@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """Quote Admin Class"""

    list_display = (
        "pk",
        "title",
        "author",
    )
    list_display_links = ("title",)
    search_fields = ("author__name", "body")
    list_filter = ("author",)
    ordering = ("pk",)

    # prepopulate slug field with person name title property
    prepopulated_fields = {"slug": ("body",)}


# person admin
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Person Admin Class"""

    list_display = ("name",)
    search_fields = ("name",)

    prepopulated_fields = {
        "slug": ("name",),
    }


# source admin
@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    """Source Admin Class"""

    list_display = ("title",)
    search_fields = ("title",)

    prepopulated_fields = {
        "slug": ("title",),
    }


# category admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category Admin Class"""

    list_display = ("title",)
    search_fields = ("title",)

    prepopulated_fields = {
        "slug": ("title",),
    }


# mediatype admin
@admin.register(MediaType)
class MediaTypeAdmin(admin.ModelAdmin):
    """MediaType Admin Class"""

    list_display = ("title",)
    search_fields = ("title",)

    prepopulated_fields = {
        "slug": ("title",),
    }
