from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class Links(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=50)
    permalink = models.TextField(unique=True)
    slug = models.SlugField(unique=True)
    shown = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Links"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("links:url_redirect", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
