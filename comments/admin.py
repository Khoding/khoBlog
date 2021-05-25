from django.contrib import admin
from django_comments.admin import CommentsAdmin

from .models import CustomComment


admin.site.unregister(CustomComment)
admin.site.register(CustomComment, CommentsAdmin)
