from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

import auto_prefetch
from simple_history.models import HistoricalRecords

from links.models import Links


class BaseFactAbstractModel(auto_prefetch.Model):
    """BaseFactAbstractModel A Base model for Facts"""

    title = models.CharField(max_length=200, help_text="Fact title")
    snippet = models.CharField(max_length=200, blank=True, default="", help_text="Short Fact description")
    description = models.TextField(blank=True, default="", help_text="Fact description")
    fact = models.TextField(default="")
    slug = models.SlugField(unique=True, default="", max_length=200, help_text="Fact slug")
    created_date = models.DateTimeField(default=timezone.now, help_text="Creation date")
    mod_date = models.DateTimeField(auto_now=True, help_text="Last modification")
    pub_date = models.DateTimeField(blank=True, null=True, help_text="Publication date")
    rnd_choice = models.IntegerField(default=0, help_text="How many times the Fact has been randomly selected")
    link = auto_prefetch.ForeignKey(Links, on_delete=models.CASCADE, null=True, blank=True)
    shown = models.BooleanField(default=True, help_text="Is it shown")
    priority = models.PositiveIntegerField(default=0)

    # Metadata about the fact
    site = auto_prefetch.ForeignKey(Site, default=1, on_delete=models.CASCADE)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def save_without_historical_record(self, *args, **kwargs):
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret

    def rnd_chosen(self):
        self.rnd_choice += 1
        self.save_without_historical_record(update_fields=["rnd_choice"])


class Fact(BaseFactAbstractModel):
    """Fact Model Class"""

    prefix = models.CharField(max_length=25, default="Fun Fact: ")
    history = HistoricalRecords()

    class Meta(BaseFactAbstractModel.Meta):
        verbose_name_plural = "Facts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_admin_update_url(self):
        return reverse("admin:facts_fact_change", kwargs={"object_id": self.pk})


class SpecificDateFact(BaseFactAbstractModel):
    """SpecificDateFact Model

    A model for a Fact that should only be shown on specific dates
    """

    SHOWING_RULE_CHOICES = [
        ("D", "date"),
        ("T", "time"),
        ("DT", "date_time"),
    ]

    showing_date = models.DateTimeField(blank=True, null=True)
    showing_rule = models.CharField(
        max_length=25,
        verbose_name="Showing Rules",
        choices=SHOWING_RULE_CHOICES,
        default="D",
    )
    show_timesince = models.BooleanField(default=True)
    is_recurrent = models.BooleanField(default=True)
    history = HistoricalRecords()

    class Meta(BaseFactAbstractModel.Meta):
        verbose_name_plural = "Specific Date Facts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_admin_update_url(self):
        return reverse("admin:facts_specificdatefact_change", kwargs={"object_id": self.pk})
