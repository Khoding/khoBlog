from django.contrib import admin, messages
from django.core import serializers
from django.http import HttpResponse
from django.utils.translation import ngettext
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from markdownx.widgets import AdminMarkdownxWidget
from simple_history.admin import SimpleHistoryAdmin

from .models import Category, Post, PostCatsLink, PostContent, Series


class PostResource(resources.ModelResource):

    class Meta:
        model = Post


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


def make_removed(modeladmin, request, queryset):
    updated = queryset.update(approbation_state='RE')
    modeladmin.message_user(request, ngettext(
        '%d post was successfully marked as removed.',
        '%d posts were successfully marked as removed.',
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


class PostContentInline(admin.TabularInline):
    model = PostContent
    extra = 0

    formfield_overrides = {
        PostContent.body: {'widget': AdminMarkdownxWidget},
    }


class PostAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = PostResource
    list_display = ('pk', 'title', 'created_date', 'published_date',
                    'slug', 'publication_state', 'featuring_state', 'featured_cat_title', 'clicks', 'language', 'is_removed')
    list_display_links = ('pk', 'title', )
    ordering = ('-pk',)
    search_fields = ('title', 'featured_title', 'slug',
                     'pk', 'withdrawn', 'featuring_state', 'url_to_article', 'url_to_article_title',)
    prepopulated_fields = {
        'slug': ('title',), }
    list_filter = ('categories', 'publication_state',
                   'featuring_state', 'published_date', 'withdrawn', 'featuring_state', 'language', 'tags',)

    fieldsets = (
        (None, {'fields': ('title', 'featured_title',
                           'description', 'author', 'slug', 'body', 'tags',)}),
        (('States'), {
         'fields': ('withdrawn', 'publication_state', 'featuring_state', 'language',)}),
        (('Post Type'), {
         'fields': ('post_image', 'url_to_article', 'url_to_article_title',)}),
        (('Dates'), {
         'fields': ('created_date', 'published_date',)}),
    )

    inlines = [PostContentInline, PostCatsLinkInline]

    actions = [make_published, make_withdrawn, make_featured, make_featured_big,
               export_as_json, make_baguette, make_english, make_other_language, make_multi_lingui]


class CommentAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'fulltitle', 'author_logged', 'author',
                    'created_date', 'approbation_state',)
    list_display_links = ('fulltitle',)
    ordering = ('created_date',)
    search_fields = ('author', 'body',)
    list_filter = ('author_logged', 'approbation_state')

    actions = [make_approved, make_removed, ]


class CategoryAdmin(SimpleHistoryAdmin):
    list_display = ('title', 'description', 'slug', 'withdrawn')
    ordering = ('-pk',)
    search_fields = ('title', 'slug', 'pk', 'withdrawn')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('withdrawn',)


@admin.register(Series)
class SeriesAdmin(SimpleHistoryAdmin):
    list_display = ('title', 'slug',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
