import auto_prefetch
from django.db import models


class Resource(auto_prefetch.Model):
    """Model for learning resources"""

    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    withdrawn = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

    def __str__(self):
        """String representation of Resource Model"""
        return self.title
