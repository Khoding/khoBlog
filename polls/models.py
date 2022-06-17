import datetime

import auto_prefetch
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Question(auto_prefetch.Model):
    """Question model"""

    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        """Return the title"""
        return self.title

    def was_published_recently(self):
        """Check if the question was published recently"""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = "pub_date"
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"

    def get_index_view_url(self):
        """Get the url for the index view"""
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("%s:index" % (content_type.app_label))


class Choice(auto_prefetch.Model):
    """Choice model"""

    question = auto_prefetch.ForeignKey(Question, on_delete=models.CASCADE, related_name="related_question")
    title = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return the title"""
        return self.title
