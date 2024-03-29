from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from khoBlog.utils.superuser_required import superuser_required_ignore_secure_mode
from portfolio.forms import (
    ProjectAddForm,
    ProjectDeleteForm,
    ProjectUpdateForm,
    SubProjectAddForm,
    SubProjectUpdateForm,
)

from .models import Project, SubProject


class ProjectListView(ListView):
    """ProjectListView Class"""

    model = Project
    template_name = "portfolio/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        """Get queryset"""
        return Project.objects.filter(deleted_at=None)

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Portfolio"
        context["description"] = "List of Projects"
        return context


class ProjectDetailView(DetailView):
    """ProjectDetailView Class"""

    model = Project
    template_name = "portfolio/project_detail.html"

    def get_object(self, queryset=None):
        """Get object"""
        obj = super(ProjectDetailView, self).get_object(queryset=queryset)
        if obj.deleted_at:
            raise Http404
        return super().get_object()

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = f"Project | {self.get_object().title}"
        context["description"] = self.get_object().description
        return context


@superuser_required_ignore_secure_mode()
class ProjectCreateView(CreateView):
    """ProjectCreateView Class"""

    model = Project
    template_name = "portfolio/create_project.html"
    form_class = ProjectAddForm

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Project"
        context["description"] = "Create a Project"
        return context


@superuser_required_ignore_secure_mode()
class ProjectUpdateView(UpdateView):
    """ProjectUpdateView Class"""

    model = Project
    template_name = "portfolio/edit_project.html"
    form_class = ProjectUpdateForm

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Project"
        context["description"] = "Update a Project"
        return context


class ProjectDeleteView(UpdateView):
    """ProjectDeleteView

    View to delete a Project

    Raises:
        PermissionDenied: [description]

    Returns:
        [type]: [description]
    """

    model = Project
    template_name = "portfolio/project_confirm_delete.html"
    form_class = ProjectDeleteForm
    success_url = reverse_lazy("portfolio:project_list")

    def get_queryset(self):
        """Get queryset"""
        if self.request.user.is_superuser:
            removing_project = get_object_or_404(Project, slug=self.kwargs["slug"])
            if self.get_form().is_valid():
                removing_project.soft_delete()
        else:
            raise PermissionDenied
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Project"
        context["description"] = "Delete a Project"
        return context


class SubProjectDetailView(DetailView):
    """SubProjectDetailView Class"""

    model = SubProject
    context_object_name = "project"
    template_name = "portfolio/project_detail.html"

    def get_object(self):
        """Get object"""
        sub = get_object_or_404(SubProject, slug=self.kwargs["subproject_slug"])
        return sub

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = f"Sub Project | {self.get_object().title}"
        context["description"] = self.get_object().description
        return context


@superuser_required_ignore_secure_mode()
class SubProjectCreateView(CreateView):
    """SubProjectCreateView Class"""

    model = SubProject
    template_name = "portfolio/create_sub_project.html"
    form_class = SubProjectAddForm

    def get_parent(self):
        """Get parent"""
        parent = get_object_or_404(Project, slug=self.kwargs["slug"])
        return parent

    def form_valid(self, form):
        """Form valid"""
        form.instance.parent_project = self.get_parent()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Project"
        context["description"] = "Create a Project"
        context["parent"] = self.get_parent()
        return context


@superuser_required_ignore_secure_mode()
class SubProjectUpdateView(UpdateView):
    """SubProjectUpdateView Class"""

    model = SubProject
    template_name = "portfolio/edit_sub_project.html"
    form_class = SubProjectUpdateForm

    def get_parent(self):
        """Get parent"""
        parent = get_object_or_404(Project, slug=self.kwargs["slug"])
        return parent

    def get_object(self):
        """Get object"""
        sub = get_object_or_404(SubProject, slug=self.kwargs["subproject_slug"])
        return sub

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Project"
        context["description"] = "Update a Project"
        context["parent"] = self.get_parent()
        return context


class SubProjectDeleteView(UpdateView):
    """SubProjectDeleteView

    View to delete a SubProject

    Raises:
        PermissionDenied: [description]

    Returns:
        [type]: [description]
    """

    model = SubProject
    template_name = "portfolio/sub_project_confirm_delete.html"
    form_class = ProjectDeleteForm
    success_url = reverse_lazy("portfolio:project_list")

    def get_object(self):
        """Get object"""
        sub = get_object_or_404(SubProject, slug=self.kwargs["subproject_slug"])
        return sub

    def get_queryset(self):
        """Get queryset"""
        if self.request.user.is_superuser:
            removing_project = self.get_object()
            if self.get_form().is_valid():
                removing_project.soft_delete()
        else:
            raise PermissionDenied
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Project"
        context["description"] = "Delete a Project"
        return context
