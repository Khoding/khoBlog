from django.db import models
from django.template.defaultfilters import slugify
from django.urls.base import reverse


class Page(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField(null=True, unique=True)
    update_date = models.DateTimeField('Last Updated', null=True, blank=True)
    page_head = models.TextField('Page head', blank=True)
    bodytext = models.TextField('Page Content', blank=True)
    main_page = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("pages:page_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
