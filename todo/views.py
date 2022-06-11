from django.urls.base import reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView
from django.views.generic.edit import CreateView

from khoBlog.utils.superuser_required import superuser_required

from .forms import TaskChangeStatusForm, TaskForm
from .models import Task


class TaskListView(ListView):
    model = Task
    template_name = "todo/list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(withdrawn=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Task List"
        context["description"] = "List of Tasks"
        return context


@superuser_required()
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/create_task.html"
    success_url = reverse_lazy("todo:task_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Task"
        context["description"] = "Create a Task"
        return context


@superuser_required()
class TaskChangeStatusView(UpdateView):
    model = Task
    form_class = TaskChangeStatusForm
    template_name = "todo/task_change_status.html"
    success_url = reverse_lazy("todo:task_list")

    def form_valid(self, form):
        print(form.cleaned_data["status"])
        self.status = form.cleaned_data["status"]
        print(form.cleaned_data["status"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Task Change status"
        context["description"] = "Change the status of a Task"
        return context


@superuser_required()
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/edit_task.html"
    success_url = reverse_lazy("todo:task_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Task"
        context["description"] = "Update a Task"
        return context


@superuser_required()
class TaskDeleteView(DeleteView):
    model = Task
    template_name = "todo/delete.html"
    success_url = reverse_lazy("todo:task_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Task"
        context["description"] = "Delete a Task"
        return context
