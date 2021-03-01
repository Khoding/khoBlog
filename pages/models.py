from django.db import models
from django.template.defaultfilters import slugify
from django.urls.base import reverse
from django.contrib.flatpages.models import FlatPage as FlatPageOld


class FlatPage(FlatPageOld):
    slug = models.SlugField(unique=True, default="")
    update_date = models.DateTimeField('Last Updated', null=True, blank=True)
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
