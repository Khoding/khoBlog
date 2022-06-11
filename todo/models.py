from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone

import auto_prefetch


class Task(auto_prefetch.Model):
    STATUS = [
        ("complete", "Complete"),
        ("incomplete", "Incomplete"),
        ("wontfix", "WONTFIX"),
        ("impossible", "IMPOSSIBLE"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200, blank=True)
    withdrawn = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now, help_text="Creation date")
    mod_date = models.DateTimeField(auto_now=True, blank=True, null=True, help_text="Last modification")
    completed_date = models.DateTimeField(
        blank=True, null=True, help_text="Completion date, completion can also mean marked as x"
    )
    status = models.CharField(choices=STATUS, max_length=10, default="incomplete")
    reason_of_status = models.TextField(blank=True, default="", help_text="Reason for status")

    def __str__(self):
        return self.title

    def status_changed(self):
        self.completed_date = timezone.now()
        self.save()

    def get_index_view_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("%s:%s_list" % (content_type.app_label, content_type.model))
