from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

import auto_prefetch
from simple_history.models import HistoricalRecords

from links.models import Links


class BaseFactAbstractModel(auto_prefetch.Model):
    """BaseFactAbstractModel

    A Base model for Facts
    """

    title = models.CharField(max_length=200, help_text="Fact title")
    snippet = models.CharField(max_length=200, blank=True, default="", help_text="Short Fact description")
    description = models.TextField(blank=True, default="", help_text="Fact description")
    fact = models.TextField(default="")
    slug = models.SlugField(unique=True, default="", max_length=200, help_text="Fact slug")
    created_date = models.DateTimeField(default=timezone.now, help_text="Creation date")
    mod_date = models.DateTimeField(auto_now=True, help_text="Last modification")
    pub_date = models.DateTimeField(blank=True, null=True, help_text="Publication date")
    link = auto_prefetch.ForeignKey(Links, on_delete=models.CASCADE, null=True, blank=True)
    prefix = models.CharField(max_length=25, default="Fun Fact: ")

    # Metadata about the fact
    site = auto_prefetch.ForeignKey(Site, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True


class Fact(BaseFactAbstractModel):
    """Fact Model

    A Model for Facts
    """

    shown = models.BooleanField(default=True, help_text="Is it shown")
    priority = models.PositiveIntegerField(default=0)
    history = HistoricalRecords()

    class Meta(BaseFactAbstractModel.Meta):
        verbose_name_plural = "Facts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
