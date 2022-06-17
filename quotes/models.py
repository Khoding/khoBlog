from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

import auto_prefetch
from simple_history.models import HistoricalRecords


class BaseQuoteAbstractModel(auto_prefetch.Model):
    """BaseQuoteAbstractModel Model Class"""

    slug = models.SlugField(unique=True, default="", max_length=200, help_text="Quote slug")
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta(auto_prefetch.Model.Meta):
        """Meta"""

        abstract = True

    # override the __str__ method to return the title of the quote
    def __str__(self):
        return self.title


# abstact auto_prefetch model for quotes
class Quote(BaseQuoteAbstractModel):
    """Quotes Model Class"""

    TO_OR_ABOUT = [
        ("to", "to"),
        ("ab", "about"),
    ]

    # Quote has a title, a body, a source, and a date, and an history of changes with an HistoricalRecords field
    author = models.ForeignKey("quotes.Person", on_delete=models.CASCADE, null=True, blank=False)
    person = models.ManyToManyField("quotes.Person", blank=True, related_name="person")
    addressing = models.ManyToManyField("quotes.Person", blank=True, related_name="addressing")
    to_or_about = models.CharField(
        max_length=2, choices=TO_OR_ABOUT, default="to", help_text="Whether the quote is addressed to or about someone"
    )
    body = models.TextField()
    source = models.ManyToManyField("quotes.Source", blank=True)
    category = models.ForeignKey("quotes.Category", on_delete=models.CASCADE, null=False, blank=False)

    history = HistoricalRecords()

    class Meta(BaseQuoteAbstractModel.Meta):
        """Meta"""

        pass

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("quotes:quote_detail", kwargs={"slug": self.slug})

    # create a title property that returns the title of the quote
    # the title is the name of the author and the body of the quote
    @property
    def title(self) -> str:
        return f"{self.author.name} - {self.body}"


# abstract auto_prefetch model for quoters
class Person(BaseQuoteAbstractModel):
    """Person Model Class"""

    name = models.CharField(max_length=255)

    history = HistoricalRecords()

    class Meta(BaseQuoteAbstractModel.Meta):
        """Meta"""

        verbose_name_plural = "People"

    # override the __str__ method to return the name of the quoter
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


# auto_prefetch model for sources
class Source(BaseQuoteAbstractModel):
    """Source Model Class"""

    DATE_TYPE_FORMAT_YEAR = "%Y"
    DATE_TYPE_FORMAT_YEAR_MONTH = "%B %Y"
    DATE_TYPE_FORMAT_FULL = "%Y-%m-%d"

    DATE_TYPE = [
        (DATE_TYPE_FORMAT_YEAR, "Year"),
        (DATE_TYPE_FORMAT_YEAR_MONTH, "Year and Month"),
        (DATE_TYPE_FORMAT_FULL, "Full Date"),
    ]

    # source has a title, an url, and an history of changes with an HistoricalRecords field
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255, blank=True, default="")
    date = models.DateField(null=True, blank=True)
    date_type = models.CharField(choices=DATE_TYPE, max_length=8, default="Y")
    linking_text = models.CharField(
        max_length=20,
        default="in",
        help_text="Defaults to in, but can be changed to on, on the, etc.",
    )
    media = models.ForeignKey("quotes.MediaType", on_delete=models.CASCADE, null=True, blank=True)

    history = HistoricalRecords()

    class Meta(BaseQuoteAbstractModel.Meta):
        """Meta"""

        pass

    # override the __str__ method to return the title of the source
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


# auto_prefetch model for categories
class Category(BaseQuoteAbstractModel):
    """Category Model Class"""

    # category has a name and an history of changes with an HistoricalRecords field
    title = models.CharField(max_length=255)

    history = HistoricalRecords()

    class Meta(BaseQuoteAbstractModel.Meta):
        """Meta"""

        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


# auto_prefetch model for media
class MediaType(BaseQuoteAbstractModel):
    """Media Model Class"""

    # media has a title, an url, and an history of changes with an HistoricalRecords field
    title = models.CharField(max_length=255)

    history = HistoricalRecords()

    class Meta(BaseQuoteAbstractModel.Meta):
        """Meta"""

        verbose_name_plural = "Media"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
