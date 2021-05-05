from django.db import models
from django_comments.abstracts import CommentAbstractModel


class CustomComment(CommentAbstractModel):
    title = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title
