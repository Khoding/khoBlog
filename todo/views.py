from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test

from .models import Todo
from .forms import TodoForm


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    todo_list = Todo.objects.order_by('id')

    form = TodoForm()

    context = {'todo_list': todo_list, 'form': form}

    return render(request, 'todo/todo.html', context)


@user_passes_test(lambda u: u.is_superuser)
@require_POST
def addTodo(request):
    form = TodoForm(request.POST)

    if form.is_valid():
        new_todo = Todo(text=request.POST['text'])
        new_todo.save()

    return redirect('todo:index')


@user_passes_test(lambda u: u.is_superuser)
def completeTodo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.complete = True
    todo.save()

    return redirect('todo:index')


@user_passes_test(lambda u: u.is_superuser)
def deleteCompleted(request):
    Todo.objects.filter(complete__exact=True).delete()

    return redirect('todo:index')


@user_passes_test(lambda u: u.is_superuser)
def deleteAll(request):
    Todo.objects.all().delete()

    return redirect('todo:index')
