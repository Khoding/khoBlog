from django.contrib import admin

from .forms import ProjectAddForm
from .models import Project, SubProject, Repository, Technology, Website


class ProjectAdmin(admin.ModelAdmin):
    """Admin class for Project"""

    form_class = ProjectAddForm
    list_display = (
        "title",
        "snippet",
        "description",
        "technology",
        "repository",
    )
    ordering = ("-pk",)
    prepopulated_fields = {"slug": ("title",)}


class WebsiteAdmin(admin.ModelAdmin):
    """Admin class for Website"""

    list_display = ("title", "url")
    ordering = ("-pk",)


class TechnologyAdmin(admin.ModelAdmin):
    """Admin class for Technology"""

    list_display = ("title", "description", "website")
    ordering = ("-pk",)


class RepositoryAdmin(admin.ModelAdmin):
    """Admin class for Repository"""

    list_display = ("title", "url")
    ordering = ("-pk",)


admin.site.register(Project, ProjectAdmin)
admin.site.register(SubProject)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Repository, RepositoryAdmin)
