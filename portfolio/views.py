from django.urls.base import reverse_lazy
from portfolio.forms import ProjectAddForm, ProjectUpdateForm
from .models import Project

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView


class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Projects'
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.model.objects.all()
        context['title'] = 'Project Detail'
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
        return context


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'portfolio/project_update.html'
    form_class = ProjectUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Project'
        context['description'] = "Update a Project"
        return context


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "portfolio/project_confirm_delete.html"
    success_url = reverse_lazy('portfolio:project_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Project'
        return context
