from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.urls import reverse
from django.template.defaultfilters import slugify


class Project(models.Model):
    title = models.CharField(max_length=100)
    snippet = models.TextField()
    description = models.TextField()
    technology = models.ForeignKey(
        'portfolio.Technology', on_delete=DO_NOTHING, related_name='technologies', null=True, blank=True)
    slug = models.SlugField(null=False, unique=True)
    website = models.ForeignKey(
        'portfolio.Website', on_delete=CASCADE, related_name='websites', null=True, blank=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Website(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.title


class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.name
