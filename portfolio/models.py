import auto_prefetch
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone


class Project(auto_prefetch.Model):
    """Model for Project"""

    title = models.CharField(max_length=100)
    snippet = models.TextField()
    description = models.TextField()
    slug = models.SlugField(unique=True, default="", max_length=200)
    start_date = models.DateTimeField("Project's start date", null=True, blank=True)
    created_date = models.DateTimeField("Creation date", default=timezone.now)
    mod_date = models.DateTimeField("Last Updated", auto_now=True)
    website = auto_prefetch.ForeignKey(
        "portfolio.Website",
        on_delete=models.CASCADE,
        related_name="websites",
        null=True,
        blank=True,
    )
    featured = models.BooleanField(default=False)
    repository = auto_prefetch.ForeignKey(
        "portfolio.Repository",
        on_delete=models.DO_NOTHING,
        related_name="repositories",
        null=True,
        blank=True,
    )
    technology = auto_prefetch.ForeignKey(
        "portfolio.Technology",
        on_delete=models.DO_NOTHING,
        related_name="technologies",
        null=True,
        blank=True,
    )
    is_removed = models.BooleanField("is removed", default=False, db_index=True, help_text=("Soft delete"))

    class Meta:
        """Meta class for Project Model Class"""

        ordering = ["pk"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})

    def get_absolute_update_url(self):
        return reverse("portfolio:project_edit", kwargs={"slug": self.slug})

    def get_absolute_delete_url(self):
        return reverse("portfolio:project_delete", kwargs={"slug": self.slug})

    def get_absolute_admin_update_url(self):
        return reverse("admin:portfolio_project_change", kwargs={"object_id": self.pk})

    def get_index_view_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("%s:%s_list" % (content_type.app_label, content_type.model))


class Website(auto_prefetch.Model):
    """Model for Website"""

    title = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.title


class Technology(auto_prefetch.Model):
    """Model for Technology"""

    title = models.CharField(max_length=100)
    description = models.TextField(default="", blank=True)
    website = models.URLField(default="", blank=True)

    class Meta:
        """Meta class for Technology Model Class"""

        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.title


class Repository(auto_prefetch.Model):
    """Model for Repository"""

    title = models.CharField(max_length=100)
    url = models.URLField()

    class Meta:
        """Meta class for Repository Model Class"""

        verbose_name_plural = "Repositories"

    def __str__(self):
        return self.title
