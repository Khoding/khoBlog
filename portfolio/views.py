from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from khoBlog.utils.superuser_required import superuser_required
from portfolio.forms import ProjectAddForm, ProjectUpdateForm, SubProjectAddForm, SubProjectUpdateForm

from .models import Project, SubProject


class ProjectListView(ListView):
    model = Project
    template_name = "portfolio/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Projects"
        context["description"] = "List of Projects"
        context["app_title"] = "Portfolio"
        context["app_direct_link"] = reverse_lazy("portfolio:project_list")
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "portfolio/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = self.model.objects.all()
        context["title"] = "Project Detail"
        context["description"] = "Details of a Project"
        context["app_title"] = "Portfolio"
        context["app_direct_link"] = reverse_lazy("portfolio:project_list")
        context["side_title"] = "Projects"
        return context


@superuser_required()
class ProjectCreateView(CreateView):
    model = Project
    template_name = "portfolio/create_project.html"
    form_class = ProjectAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Project"
        context["description"] = "Create a Project"
        context["app_title"] = "Portfolio"
        context["app_direct_link"] = reverse_lazy("portfolio:project_list")
        return context


@superuser_required()
class ProjectUpdateView(UpdateView):
    model = Project
    template_name = "portfolio/edit_project.html"
    form_class = ProjectUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Project"
        context["description"] = "Update a Project"
        context["app_title"] = "Portfolio"
        context["app_direct_link"] = reverse_lazy("portfolio:project_list")
        return context


@superuser_required()
class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "portfolio/project_confirm_delete.html"
    success_url = reverse_lazy("portfolio:project_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Project"
        context["description"] = "Delete a Project"
        context["app_title"] = "Portfolio"
        context["app_direct_link"] = reverse_lazy("portfolio:project_list")
        return context


class SubProjectDetailView(DetailView):
    model = SubProject
    template_name = "portfolio/sub_project_detail.html"

    def get_object(self):
        sub = get_object_or_404(SubProject, slug=self.kwargs["subproject_slug"])
        return sub

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Project Detail"
        context["description"] = "Details of a Project"
        context["app_title"] = "Portfolio"
        context["app_direct_link"] = reverse_lazy("portfolio:project_list")
        context["side_title"] = "Projects"
        return context


@superuser_required()
class SubProjectCreateView(CreateView):
    model = SubProject
    template_name = "portfolio/create_sub_project.html"
    form_class = SubProjectAddForm

    def get_parent(self):
        parent = get_object_or_404(Project, slug=self.kwargs["slug"])
        return parent

    def form_valid(self, form):
        form.instance.parent_project = self.get_parent()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Project"
        context["description"] = "Create a Project"
        context["parent"] = self.get_parent()
        context["app_title"] = "Portfolio"
        context["app_direct_link"] = reverse_lazy("portfolio:project_list")
        return context


@superuser_required()
class SubProjectUpdateView(UpdateView):
    model = SubProject
    template_name = "portfolio/edit_sub_project.html"
    form_class = SubProjectUpdateForm

    def get_parent(self):
        parent = get_object_or_404(Project, slug=self.kwargs["slug"])
        return parent

    def get_object(self):
        sub = get_object_or_404(SubProject, slug=self.kwargs["subproject_slug"])
        return sub

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Project"
        context["description"] = "Update a Project"
        context["parent"] = self.get_parent()
        context["app_title"] = "Portfolio"
        context["app_direct_link"] = reverse_lazy("portfolio:project_list")
        return context


@superuser_required()
class SubProjectDeleteView(DeleteView):
    model = SubProject
    template_name = "portfolio/sub_project_confirm_delete.html"
    success_url = reverse_lazy("portfolio:project_list")

    def get_object(self):
        sub = get_object_or_404(SubProject, slug=self.kwargs["subproject_slug"])
        return sub

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Project"
        context["description"] = "Delete a Project"
        context["app_title"] = "Portfolio"
        context["app_direct_link"] = reverse_lazy("portfolio:project_list")
        return context
