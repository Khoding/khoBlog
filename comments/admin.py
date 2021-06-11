from comments.forms import AdminForm
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_comments.admin import CommentsAdmin

from .models import CustomComment


class CommentsAdmin(CommentsAdmin):
    form = AdminForm

    fieldsets = (
        (
            None,
            {'fields': ('content_type', 'object_pk', 'site', 'parent',)}
        ),
        (
            _('Content'),
            {'fields': ('user', 'user_name', 'user_email',
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


admin.site.unregister(CustomComment)
admin.site.register(CustomComment, CommentsAdmin)
