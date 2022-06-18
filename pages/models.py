from django.contrib.contenttypes.models import ContentType
from django.contrib.sitemaps import ping_google
from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.urls.base import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import auto_prefetch
from simple_history.models import HistoricalRecords
from taggit_selectize.managers import TaggableManager

from custom_taggit.models import CustomTaggedItem


class Page(auto_prefetch.Model):
    """Page model"""

    FEATURING_CHOICES = [
        ("F", "Featured"),
        ("SF", "Super Featured"),
        ("N", "Not Featured"),
    ]

    title = models.CharField(_("title"), max_length=200)
    content = models.TextField(_("content"), blank=True)
    description = models.TextField(blank=True, default="")
    page_head = models.TextField("Page head", blank=True)
    slug = models.SlugField(unique=True, default="", max_length=200)
    created_date = models.DateTimeField("Creation date", default=timezone.now)
    mod_date = models.DateTimeField("Last Updated", auto_now=True)
    main_page = models.BooleanField(default=False)
    featuring_state = models.CharField(
        max_length=25,
        verbose_name="Featuring",
        choices=FEATURING_CHOICES,
        default="N",
        help_text="Featuring state",
    )
    enable_comments = models.BooleanField(_("enable comments"), default=True)
    withdrawn = models.BooleanField(default=False)
    template_name = models.CharField(
        _("template name"),
        max_length=70,
        blank=True,
        help_text=_(
            "Example: pages/contact_page.html”. If this isn't provided, " "the system will use pages/default.html”."
        ),
    )
    registration_required = models.BooleanField(
        _("registration required"),
        help_text=_("If this is checked, only logged-in users will be able to view the page."),
        default=False,
    )
    sites = models.ManyToManyField(Site, verbose_name=_("sites"))
    tags = TaggableManager(blank=True, through=CustomTaggedItem)
    deleted_at = models.DateTimeField(blank=True, null=True, help_text="Deletion date for soft delete")

    history = HistoricalRecords()

    class Meta:
        """Meta class for Page Model"""

        ordering = ["pk"]

    def __str__(self):
        """String representation of the model"""
        return self.title

    def save(self, *args, **kwargs):
        """Override save method"""
        try:
            ping_google()
        except Exception:  # skipcq: PYL-W0703
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get the url for the detail view"""
        return reverse("pages:page_detail", kwargs={"slug": self.slug})

    def get_absolute_update_url(self):
        """Get the url for the update view"""
        return reverse("pages:page_edit", kwargs={"slug": self.slug})

    def get_absolute_delete_url(self):
        """Get the url for the delete view"""
        return reverse("pages:page_delete", kwargs={"slug": self.slug})

    def get_absolute_admin_update_url(self):
        """Get the url for the admin update view"""
        return reverse("admin:pages_page_change", kwargs={"object_id": self.pk})

    def soft_delete(self):
        """Soft delete the page"""
        self.deleted_at = timezone.now()
        self.save()

    def get_index_view_url(self):
        """Get the url for the index view"""
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("%s:index" % (content_type.app_label))
