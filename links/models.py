import auto_prefetch
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class Links(auto_prefetch.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=50)
    permalink = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, default="", max_length=200)
    shown = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Links"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("links:url_redirect", kwargs={"slug": self.slug})
