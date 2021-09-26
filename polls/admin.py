from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ("title", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["title"]


admin.site.register(Question, QuestionAdmin)
