from django.db import models
from django_comments.abstracts import CommentAbstractModel


class CustomComment(CommentAbstractModel):
    title = models.CharField(max_length=200, null=True, blank=True)
    alias_user = models.CharField(max_length=200, null=True, blank=True,
                                  help_text="You can add an Alias Name to your comment if you wish to be "
                                  'incognito (note that Moderators can still know it\'s you)', verbose_name="alias_name")
    comment = models.TextField()

    def __str__(self):
        return f'{self.content_object.title} - {self.title} • {self.comment}'
