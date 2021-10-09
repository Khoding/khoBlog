from django.db import models

import auto_prefetch
from django_comments.abstracts import CommentAbstractModel
from django_comments_xtd.models import XtdComment


class CustomComment(CommentAbstractModel):
    title = models.CharField(max_length=200, default="")
    alias_user = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="You can add an Alias Name to your comment if you wish to be "
        "incognito (note that Moderators can still know it's you)",
        verbose_name="alias_name",
    )
    comment = models.TextField()
    parent = auto_prefetch.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="comment_children",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["submit_date"]

    def __str__(self):
        return self.full_title

    @property
    def full_title(self):
        full_t = ""
        if self.content_object:
            full_t = full_t + str(self.content_type.model) + " - " + str(self.content_object.title) + " - "
        if self.title:
            full_t = full_t + self.title + " - "
        full_t = full_t + self.comment[:25]
        return full_t

    def get_absolute_url(self, anchor_pattern="#comment-%(id)s"):
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)


class CustomCommentXTD(XtdComment):
    title = models.CharField(max_length=200, blank=True, default="")
    alias_user = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="You can add an Alias Name to your comment if you wish to be "
        "incognito (note that Moderators can still know it's you)",
        verbose_name="alias_name",
    )

    def __str__(self):
        return self.full_title

    @property
    def full_title(self):
        full_t = ""
        if self.content_object:
            full_t = full_t + str(self.content_type.model) + " - " + str(self.content_object.title) + " - "
        if self.title:
            full_t = full_t + self.title + " - "
        full_t = full_t + self.comment[:25]
        return full_t

    def get_absolute_url(self, anchor_pattern="#comment-%(id)s"):
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)
