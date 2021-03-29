from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    complete = models.BooleanField(default=False)
    todo_group = models.ForeignKey(
        'todo.TodoGroup', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class TodoGroup(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
