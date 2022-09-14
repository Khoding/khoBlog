from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.models import F

import auto_prefetch


class URL(auto_prefetch.Model):
    """URL model"""

    title = models.CharField(max_length=200, unique=True)
    full_url = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, default="", max_length=200)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        """Return the title of the url"""
        return self.title

    def save(self, *args, **kwargs):
        """Save"""
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get absolute url"""
        return reverse("shortener:url_redirect", kwargs={"slug": self.slug})

    def clicked(self):
        """Clicked"""
        self.clicks = F("clicks") + 1
        self.save()
