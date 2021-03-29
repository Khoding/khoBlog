from django.contrib import admin

from .models import Todo, TodoGroup

admin.site.register(Todo)
admin.site.register(TodoGroup)
