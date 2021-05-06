from django.db import models
from django.template.defaultfilters import slugify
from django.urls.base import reverse
from django.contrib.flatpages.models import FlatPage as FlatPageOld
from django.utils import timezone


class FlatPage(FlatPageOld):
    slug = models.SlugField(unique=True, default="", max_length=200)
    modified_date = models.DateTimeField('Last Updated', auto_now=True)
    created_date = models.DateTimeField('Creation date', default=timezone.now)
    page_head = models.TextField('Page head', blank=True)
    main_page = models.BooleanField(default=False)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("pages:page_detail", kwargs={"slug": self.slug})
