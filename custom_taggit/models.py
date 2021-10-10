from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from taggit.models import GenericTaggedItemBase, TagBase


class CustomTag(TagBase):
    withdrawn = models.BooleanField(default=False)

    class Meta:
        ordering = ["pk"]
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def get_absolute_url(self):
        return reverse("blog:post_tagged_with", kwargs={"slug": self.slug})

    def get_absolute_update_url(self):
        return reverse("blog:tag_edit", kwargs={"slug": self.slug})

    def get_absolute_admin_update_url(self):
        return reverse("admin:custom_taggit_customtag_change", kwargs={"object_id": self.pk})

    def get_index_view_url(self):
        return reverse("blog:tag_list")


class CustomTaggedItem(GenericTaggedItemBase):
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
