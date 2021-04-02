from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse

from .models import Task
from .forms import TaskForm


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    tasks = Task.objects.all()

    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('todo:list'))

    context = {'tasks': tasks, 'form': form,
               'title': 'Todo List'}
    return render(request, 'todo/list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def updateTask(request, pk):
    task = Task.objects.get(id=pk)

    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse('todo:list'))

    context = {'form': form,
               'title': 'Update Task'}

    return render(request, 'todo/update_task.html', context)


@user_passes_test(lambda u: u.is_superuser)
def deleteTask(request, pk):
    task = Task.objects.get(id=pk)

    if request.method == 'POST':
        task.delete()
        return redirect(reverse('todo:list'))

    context = {
        'task': task,
        'title': 'Delete Task'
    }
    return render(request, 'todo/delete.html', context)
