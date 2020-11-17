from django.contrib import admin

from .models import Project, Technology, Website
from .forms import ProjectForm


class ProjectAdmin(admin.ModelAdmin):
    form_class = ProjectForm
    list_display = ('title', 'snippet', 'description',
                    'technology')
    ordering = ('-pk',)
    prepopulated_fields = {'slug': ('title',)}


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    ordering = ('-pk',)


class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'website')
    ordering = ('-pk',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Technology, TechnologyAdmin)
