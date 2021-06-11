from django.db import models
from django_comments.abstracts import CommentAbstractModel


class CustomComment(CommentAbstractModel):
    title = models.CharField(max_length=200, null=True, blank=True)
    alias_user = models.CharField(max_length=200, null=True, blank=True,
                                  help_text="You can add an Alias Name to your comment if you wish to be "
                                  'incognito (note that Moderators can still know it\'s you)', verbose_name="alias_name")
    comment = models.TextField()

    class Meta:
        ordering = ['-submit_date']

    def __str__(self):
        return self.full_title

    @property
    def full_title(self):
        full_t = ''
        if self.content_object:
            full_t = full_t + str(self.content_type.model) + \
                ' - ' + str(self.content_object.title) + ' - '
        elif self.title:
            full_t = self.title + ' - '
        full_t = full_t + self.comment
        return full_t

    def get_absolute_url(self, anchor_pattern="#comment-%(id)s"):
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)
