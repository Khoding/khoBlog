from django.urls.base import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from portfolio.forms import ProjectAddForm, ProjectUpdateForm

from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Projects'
        context['description'] = "List of Projects"
        context['app_title'] = 'Portfolio'
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.model.objects.all()
        context['title'] = 'Project Detail'
        context['description'] = "Details of a Project"
        context['app_title'] = 'Portfolio'
        context['side_title'] = 'Projects'
        return context


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'portfolio/project_add.html'
    form_class = ProjectAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Project'
        context['description'] = "Create a Project"
        context['app_title'] = 'Portfolio'
        return context


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'portfolio/project_update.html'
    form_class = ProjectUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Project'
        context['description'] = "Update a Project"
        context['app_title'] = 'Portfolio'
        return context


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "portfolio/project_confirm_delete.html"
    success_url = reverse_lazy('portfolio:project_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Project'
        context['description'] = "Delete a Project"
        context['app_title'] = 'Portfolio'
        return context
