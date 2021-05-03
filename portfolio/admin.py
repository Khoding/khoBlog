from django.contrib import admin

from .models import Project, Technology, Website, Repository
from .forms import ProjectAddForm


class ProjectAdmin(admin.ModelAdmin):
    form_class = ProjectAddForm
    list_display = ('title', 'snippet', 'description',
                    'technology', 'repository',)
    ordering = ('-pk',)
    prepopulated_fields = {'slug': ('title',)}


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    ordering = ('-pk',)


class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'website')
    ordering = ('-pk',)


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    ordering = ('-pk',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Repository, RepositoryAdmin)
