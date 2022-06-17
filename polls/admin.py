from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Inline class for Choice"""

    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    """Admin class for Question"""

    fieldsets = [
        (None, {"fields": ["title"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ("title", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["title"]


admin.site.register(Question, QuestionAdmin)
