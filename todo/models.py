import auto_prefetch
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


class Task(auto_prefetch.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200, blank=True)
    complete = models.BooleanField(default=False)
    withdrawn = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_index_view_url(self):
        content_type = ContentType.objects.get_for_model(
            self.__class__)
        return reverse("%s:%s_list" % (content_type.app_label, content_type.model))
