from django.contrib import admin, messages
from django.core import serializers
from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import ngettext
from markdownx.widgets import AdminMarkdownxWidget

from .models import Category, Comment, Post


def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


def make_published(modeladmin, request, queryset):
    updated = queryset.update(published_date=timezone.now())
    modeladmin.message_user(request, ngettext(
        '%d post was successfully marked as published.',
        '%d posts were successfully marked as published.',
        updated,
    ) % updated, messages.SUCCESS)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured_title', 'created_date', 'published_date', 'slug', 'get_categories',
                    'private', 'featured',)
    ordering = ('-pk',)
    search_fields = ('title', 'featured_title', 'slug',
                     'pk', 'private', 'featured',)
    prepopulated_fields = {'slug': ('title',)}

    formfield_overrides = {
        Post.body: {'widget': AdminMarkdownxWidget},
    }

    actions = [make_published, export_as_json]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_date')
    ordering = ('-author',)
    search_fields = ('author', 'message',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug', 'private')
    ordering = ('-pk',)
    search_fields = ('title', 'slug', 'pk', 'private')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
