from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic.edit import DeleteView

from .models import Todo, TodoGroup
from .forms import TodoForm


def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass

    return wrapper


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    todo_list = Todo.objects.order_by('id')

    form = TodoForm()

    context = {'todo_list': todo_list, 'form': form, 'title': 'Todo List'}

    return render(request, 'todo/todo.html', context)


@user_passes_test(lambda u: u.is_superuser)
@require_POST
def addTodo(request):
    form = TodoForm(request.POST)

    if form.is_valid():
        new_todo = Todo(
            title=request.POST['title'], description=request.POST['description'])
        new_todo.save()

    return redirect('todo:index')


@ user_passes_test(lambda u: u.is_superuser)
def completion(request, pk):
    todo = Todo.objects.get(pk=pk)
    todo.complete = (True, False)[todo.complete]
    todo.save()
    return redirect('todo:index')


@ superuser_required()
class TodoDeleteView(DeleteView):
    model = Todo
    template_name = "todo/todo_confirm_delete.html"
    success_url = reverse_lazy('todo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Todo'
        return context


@ user_passes_test(lambda u: u.is_superuser)
def deleteCompleted(request):
    Todo.objects.filter(complete=True).delete()

    return redirect('todo:index')


@ user_passes_test(lambda u: u.is_superuser)
def deleteAll(request):
    Todo.objects.all().delete()

    return redirect('todo:index')
