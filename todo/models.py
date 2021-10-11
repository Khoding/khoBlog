from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone

import auto_prefetch


class Task(auto_prefetch.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200, blank=True)
    complete = models.BooleanField(default=False)
    withdrawn = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now, help_text="Creation date")
    mod_date = models.DateTimeField(blank=True, null=True, help_text="Last modification")
    completed_date = models.DateTimeField(blank=True, null=True, help_text="Completion date")

    def __str__(self):
        return self.title

    def make_completed(self):
        self.complete = True
        self.mod_date = timezone.now()
        self.completed_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("todo:complete_task_confirmed", kwargs={"pk": self.pk})

    def get_index_view_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("%s:%s_list" % (content_type.app_label, content_type.model))
