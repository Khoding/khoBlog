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
    slug = models.SlugField(unique=True, default="", max_length=200)
    website = models.ForeignKey(
        'portfolio.Website', on_delete=CASCADE, related_name='websites', null=True, blank=True)
    featured = models.BooleanField(default=False)
    repository = models.ForeignKey(
        'portfolio.Repository', on_delete=DO_NOTHING, related_name='repositories', null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})


class Website(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.title


class Technology(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)
    website = models.URLField(default='', blank=True)

    class Meta:
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.title


class Repository(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()

    class Meta:
        verbose_name_plural = "Repositories"

    def __str__(self):
        return self.title
