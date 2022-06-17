from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

import auto_prefetch
from simple_history.models import HistoricalRecords


class BasePortfolioAbstractModel(auto_prefetch.Model):
    """Abstract Model for Portfolio"""

    class Meta(auto_prefetch.Model.Meta):
        """Meta"""

        abstract = True

    title = models.CharField(max_length=100)
    snippet = models.TextField(default="")
    description = models.TextField(default="")
    learned = models.TextField(default="")
    slug = models.SlugField(unique=True, default="", max_length=200)
    start_date = models.DateTimeField("Project's start date", null=True, blank=True)
    created_date = models.DateTimeField("Creation date", default=timezone.now)
    mod_date = models.DateTimeField("Last Updated", auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, help_text="Deletion date for soft delete")


class Project(BasePortfolioAbstractModel):
    """Model for Project"""

    featured = models.BooleanField(default=False)
    history = HistoricalRecords()
    website = auto_prefetch.ForeignKey(
        "portfolio.Website",
        on_delete=models.CASCADE,
        related_name="websites",
        null=True,
        blank=True,
    )
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

    class Meta(BasePortfolioAbstractModel.Meta):
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

    @property
    def get_sub_projects(self):
        sub_projects = self.sub_project.filter(deleted_at=None)
        return sub_projects

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def get_index_view_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("%s:%s_list" % (content_type.app_label, content_type.model))


class SubProject(BasePortfolioAbstractModel):
    """Model for SubProject"""

    parent_project = auto_prefetch.ForeignKey(
        "portfolio.Project",
        on_delete=models.CASCADE,
        related_name="sub_project",
        blank=True,
        null=True,
    )
    link_in_repo = models.CharField(max_length=255, default="", blank=True)
    featured = models.BooleanField(default=False)

    class Meta(BasePortfolioAbstractModel.Meta):
        """Meta class for SubProject Model Class"""

        ordering = ["pk"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "portfolio:sub_project_detail", kwargs={"slug": self.parent_project.slug, "subproject_slug": self.slug}
        )

    def get_absolute_update_url(self):
        return reverse(
            "portfolio:sub_project_edit", kwargs={"slug": self.parent_project.slug, "subproject_slug": self.slug}
        )

    def get_absolute_delete_url(self):
        return reverse(
            "portfolio:sub_project_delete", kwargs={"slug": self.parent_project.slug, "subproject_slug": self.slug}
        )

    def get_absolute_admin_update_url(self):
        return reverse("admin:portfolio_subproject_change", kwargs={"object_id": self.pk})

    @property
    def full_title(self) -> str:
        fulltitle = ""
        fulltitle = self.parent_project.title + " " + self.title
        return fulltitle

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

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
