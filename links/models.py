import auto_prefetch
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class BaseLinkAbstractModel(auto_prefetch.Model):
    """
    An abstract base class that any custom link models probably should
    subclass.
    """

    # Content-object field
    content_type = auto_prefetch.ForeignKey(
        ContentType,
        verbose_name=_("content type"),
        related_name="content_type_set_for_%(class)s",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    object_pk = models.CharField(_("object ID"), db_index=True, max_length=64, blank=True, null=True)
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    index = models.BooleanField(default=False)

    # Metadata about the link
    site = auto_prefetch.ForeignKey(Site, on_delete=models.CASCADE)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True

    def get_content_object_url(self):
        """
        Get a URL suitable for redirecting to the content object.
        """
        return reverse("links:link-url-redirect", args=(self.content_type, self.object_pk))


class Links(BaseLinkAbstractModel):
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=50)
    permalink = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True, default="", max_length=200)
    shown = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=0)

    class Meta(BaseLinkAbstractModel.Meta):
        verbose_name_plural = "Links"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("links:url_redirect", kwargs={"slug": self.slug})

    def get_content_object_url(self):
        """
        Get a URL suitable for redirecting to the content object.
        """
        return reverse("links:link-url-redirect", args=(self.content_type, self.object_pk))

    def get_absolute_permalink(self):
        self.permalink = self.permalink + "/"
        return self.permalink
