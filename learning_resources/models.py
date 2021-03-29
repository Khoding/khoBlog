from django.db import models


class Resource(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title
