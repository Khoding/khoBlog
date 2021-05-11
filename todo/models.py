import auto_prefetch
from django.db import models


class Task(auto_prefetch.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200, blank=True)
    complete = models.BooleanField(default=False)
    withdrawn = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
