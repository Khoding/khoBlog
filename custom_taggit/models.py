from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField
from taggit.models import GenericTaggedItemBase, TagBase


class CustomTag(TagBase):
    """CustomTag model extending TagBase"""

    COLOR_PALETTE = [
        ("#444F99", "liberty"),
        ("#F1C40F", "yellow"),
        ("#2ECC71", "emerald"),
        ("#3498DB", "carolina"),
        ("#9B8383", "cinereous"),
        ("#DF4232", "cinnabar"),
    ]

    color = ColorField(samples=COLOR_PALETTE, default="#9B8383")
    withdrawn = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True, help_text="Deletion date for soft delete")

    class Meta:
        """Meta"""

        ordering = ["pk"]
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def get_absolute_url(self):
        """Get absolute URL of Tag"""
        return reverse("custom_taggit:post_tagged_with", kwargs={"slug": self.slug})

    def get_absolute_update_url(self):
        """Get absolute URL of Tag"""
        return reverse("custom_taggit:tag_edit", kwargs={"slug": self.slug})

    def get_absolute_admin_update_url(self):
        """Get absolute URL of Tag"""
        return reverse("admin:custom_taggit_customtag_change", kwargs={"object_id": self.pk})

    def get_index_view_url(self):
        """Get index view URL of Tag"""
        return reverse("custom_taggit:tag_list")


class CustomTaggedItem(GenericTaggedItemBase):
    """CustomTaggedItem model extending GenericTaggedItemBase"""

    # TaggedWhatever can also extend TaggedItemBase or a combination of
    # both TaggedItemBase and GenericTaggedItemBase. GenericTaggedItemBase
    # allows using the same tag for different kinds of objects, in this
    # example Food and Drink.

    # Here is where you provide your custom Tag class.
    tag = models.ForeignKey(
        CustomTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )
