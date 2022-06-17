from django.db import models

from django_comments_xtd.models import XtdComment


class CustomCommentXTD(XtdComment):
    """Custom comment model"""

    title = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        """__str__"""
        return self.full_title

    @property
    def full_title(self):
        """Get full title of Comment"""
        full_t = ""
        if self.content_object:
            full_t = full_t + str(self.content_type.model) + " - " + str(self.content_object.title) + " - "
        if self.title:
            full_t = full_t + self.title + " - "
        full_t = full_t + self.comment[:25]
        return full_t

    def get_absolute_url(self, anchor_pattern="#comment-%(id)s"):
        """Get absolute url for Comment Model"""
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)
