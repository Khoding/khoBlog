from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django_comments.admin import CommentsAdmin
from django_comments_xtd.admin import XtdCommentsAdmin

from comments.forms import AdminForm

from .models import CustomComment, CustomCommentXTD


def make_site_khoblog(modeladmin, request, queryset):
    updated = queryset.update(site_id=1)
    modeladmin.message_user(request, ngettext(
        '%d comment was successfully added to site khoblog.',
        '%d comments were successfully added to site khoblog.',
        updated,
    ) % updated, messages.SUCCESS)


def make_site_localhost(modeladmin, request, queryset):
    updated = queryset.update(site_id=2)
    modeladmin.message_user(request, ngettext(
        '%d comment was successfully added to site localhost.',
        '%d comments were successfully added to site localhost.',
        updated,
    ) % updated, messages.SUCCESS)


class CommentsAdmin(CommentsAdmin):
    form = AdminForm

    list_display = ('pk', 'full_title', 'name', 'content_type', 'object_pk',
                    'ip_address', 'submit_date', 'is_public', 'is_removed', 'parent',)
    list_display_links = ('full_title',)
    ordering = ('pk',)

    fieldsets = (
        (
            None,
            {'fields': ('content_type', 'object_pk', 'site', 'parent',)}
        ),
        (
            _('Content'),
            {'fields': ('title', 'user', 'alias_user', 'user_name', 'user_email',
                        'user_url', 'comment')}
        ),
        (
            _('Metadata'),
            {'fields': ('submit_date', 'ip_address',
                        'is_public', 'is_removed')}
        ),
    )

    list_filter = ('submit_date', 'site', 'is_public',
                   'is_removed',)

    actions = ["flag_comments", "approve_comments",
               "remove_comments", make_site_khoblog, make_site_localhost]


class CommentsXTDAdmin(XtdCommentsAdmin):
    list_display = ('cid', 'thread_level', 'nested_count', 'name',
                    'content_type', 'object_pk', 'ip_address', 'submit_date',
                    'followup', 'is_public', 'is_removed')
    list_display_links = ('cid',)
    list_filter = ('content_type', 'is_public', 'is_removed', 'followup')
    fieldsets = (
        (None, {'fields': ('content_type', 'object_pk', 'site')}),
        ('Content', {'fields': ('title', 'user', 'alias_user', 'user_name', 'user_email',
                                'user_url', 'comment', 'followup')}),
        ('Metadata', {'fields': ('submit_date', 'ip_address',
                                 'is_public', 'is_removed')}),
    )
    date_hierarchy = 'submit_date'
    ordering = ('thread_id', 'order')
    search_fields = ['object_pk', 'user__username', 'user_name', 'user_email',
                     'comment']

    list_filter = ('submit_date', 'site', 'is_public',
                   'is_removed',)

    actions = ["flag_comments", "approve_comments",
               "remove_comments", make_site_khoblog, make_site_localhost]


admin.site.unregister(CustomComment)
# admin.site.register(CustomComment, CommentsAdmin)
admin.site.register(CustomCommentXTD, CommentsXTDAdmin)
