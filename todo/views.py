from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic import UpdateView, DeleteView, ListView
from django.views.generic.edit import CreateView

from .models import Task
from .forms import TaskForm

from django.contrib.auth.mixins import UserPassesTestMixin


def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass

    return wrapper


class TaskListView(ListView):
    model = Task
    template_name = 'todo/list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(withdrawn=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Task List'
        return context


@superuser_required()
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo/create_task.html'
    success_url = reverse_lazy('todo:list')

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Task'
        return context


@superuser_required()
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/update_task.html"
    success_url = reverse_lazy('todo:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Task'
        return context


@superuser_required()
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'todo/delete.html'
    success_url = reverse_lazy('todo:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Task'
        return context
