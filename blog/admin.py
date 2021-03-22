from django.contrib import admin, messages
from django.core import serializers
from django.http import HttpResponse
from django.utils.translation import ngettext
from markdownx.widgets import AdminMarkdownxWidget

from .models import Category, Comment, Post, PostCatsLink


def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


def make_published(modeladmin, request, queryset):
    updated = queryset.update(publication_state='P')
    modeladmin.message_user(request, ngettext(
        '%d post was successfully marked as published.',
        '%d posts were successfully marked as published.',
        updated,
    ) % updated, messages.SUCCESS)


def make_withdrawn(modeladmin, request, queryset):
    updated = queryset.update(publication_state='W')
    modeladmin.message_user(request, ngettext(
        '%d post was successfully marked as withdrawn.',
        '%d posts were successfully marked as withdrawn.',
        updated,
    ) % updated, messages.SUCCESS)


def make_featured(modeladmin, request, queryset):
    updated = queryset.update(featuring_state='F')
    modeladmin.message_user(request, ngettext(
        '%d post was successfully marked as featured.',
        '%d posts were successfully marked as featured.',
        updated,
    ) % updated, messages.SUCCESS)


def make_big(modeladmin, request, queryset):
    updated = queryset.update(featuring_state='B')
    modeladmin.message_user(request, ngettext(
        '%d post was successfully marked as big.',
        '%d posts were successfully marked as big.',
        updated,
    ) % updated, messages.SUCCESS)


def make_featured_big(modeladmin, request, queryset):
    updated = queryset.update(featuring_state='FB')
    modeladmin.message_user(request, ngettext(
        '%d post was successfully marked as featured big.',
        '%d posts were successfully marked as featured big.',
        updated,
    ) % updated, messages.SUCCESS)


def make_approved(modeladmin, request, queryset):
    updated = queryset.update(approbation_state='AP')
    modeladmin.message_user(request, ngettext(
        '%d post was successfully marked as approved.',
        '%d posts were successfully marked as approved.',
        updated,
    ) % updated, messages.SUCCESS)


def make_baguette(modeladmin, request, queryset):
    updated = queryset.update(language='FR')
    modeladmin.message_user(request, ngettext(
        '%d post was successfully marked as Language Baguette.',
        '%d posts were successfully marked as Language Baguette.',
        updated,
    ) % updated, messages.SUCCESS)


def make_english(modeladmin, request, queryset):
    updated = queryset.update(language='EN')
    modeladmin.message_user(request, ngettext(
        '%d post was successfully marked as Language English.',
        '%d posts were successfully marked as Language English.',
        updated,
    ) % updated, messages.SUCCESS)


def make_other_language(modeladmin, request, queryset):
    updated = queryset.update(language='OL')
    modeladmin.message_user(request, ngettext(
        '%d post was successfully marked as Another Language.',
        '%d posts were successfully marked as Another Language.',
        updated,
    ) % updated, messages.SUCCESS)


def make_multi_lingui(modeladmin, request, queryset):
    updated = queryset.update(language='ML')
    modeladmin.message_user(request, ngettext(
        '%d post was successfully marked as Multi Linguistic.',
        '%d posts were successfully marked as Multi Linguistic.',
        updated,
    ) % updated, messages.SUCCESS)


class PostCatsLinkInline(admin.TabularInline):
    model = PostCatsLink
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'published_date',
                    'slug', 'publication_state', 'featuring_state', 'clicks', 'language',)
    ordering = ('-pk',)
    search_fields = ('title', 'featured_title', 'slug',
                     'pk', 'withdrawn', 'featured', 'big', 'url_post_type', 'url_post_type_name',)
    prepopulated_fields = {
        'slug': ('title',), }
    list_filter = ('categories', 'publication_state',
                   'featuring_state', 'published_date', 'withdrawn', 'featured', 'big', 'language',)

    fieldsets = (
        (None, {'fields': ('title', 'featured_title',
                           'description', 'author', 'slug', 'body',)}),
        (('States'), {
         'fields': ('withdrawn', 'featured', 'big', 'publication_state', 'featuring_state', 'language',)}),
        (('Post Type'), {
         'fields': ('post_image', 'url_post_type', 'url_post_type_name',)}),
        (('Dates'), {
         'fields': ('created_date', 'published_date',)}),
    )

    inlines = [PostCatsLinkInline, ]

    formfield_overrides = {
        Post.body: {'widget': AdminMarkdownxWidget},
    }

    actions = [make_published, make_withdrawn, make_featured,
               make_big, make_featured_big, export_as_json, make_baguette, make_english, make_other_language, make_multi_lingui]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_logged', 'author',
                    'created_date', 'approbation_state',)
    ordering = ('-author_logged', '-author',)
    search_fields = ('author', 'message',)
    list_filter = ('author_logged', 'approbation_state')

    actions = [make_approved, ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug', 'withdrawn')
    ordering = ('-pk',)
    search_fields = ('title', 'slug', 'pk', 'withdrawn')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('withdrawn',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
