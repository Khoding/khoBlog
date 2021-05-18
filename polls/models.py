import datetime
import auto_prefetch
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


class Question(auto_prefetch.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def get_index_view_url(self):
        content_type = ContentType.objects.get_for_model(
            self.__class__)
        return reverse("%s:index" % (content_type.app_label))


class Choice(auto_prefetch.Model):
    question = auto_prefetch.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="related_question")
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
