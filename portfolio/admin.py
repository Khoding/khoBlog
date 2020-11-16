from django.contrib import admin

from .models import Project
from .forms import ProjectForm


class ProjectAdmin(admin.ModelAdmin):
    form_class = ProjectForm
    list_display = ('title', 'description',
                    'technology')
    ordering = ('-pk',)


admin.site.register(Project, ProjectAdmin)
