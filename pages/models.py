from custom_taggit.models import CustomTaggedItem
import auto_prefetch
from django.contrib.contenttypes.models import ContentType
from django.contrib.flatpages.models import FlatPage as FlatPageOld
from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.urls.base import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from taggit.managers import TaggableManager


class FlatPage(FlatPageOld):
    slug = models.SlugField(unique=True, default="", max_length=200)
    modified_date = models.DateTimeField('Last Updated', auto_now=True)
    created_date = models.DateTimeField('Creation date', default=timezone.now)
    page_head = models.TextField('Page head', blank=True)
    main_page = models.BooleanField(default=False)
    description = models.TextField(blank=True, default="")
    withdrawn = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("pages:page_detail", kwargs={"slug": self.slug})

    def get_index_view_url(self):
        content_type = ContentType.objects.get_for_model(
            self.__class__)
        return reverse("%s:index" % (content_type.app_label))


class Page(auto_prefetch.Model):
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'), blank=True)
    description = models.TextField(blank=True, default="")
    page_head = models.TextField('Page head', blank=True)
    slug = models.SlugField(unique=True, default="", max_length=200)
    created_date = models.DateTimeField('Creation date', default=timezone.now)
    modified_date = models.DateTimeField('Last Updated', auto_now=True)
    main_page = models.BooleanField(default=False)
    enable_comments = models.BooleanField(_('enable comments'), default=True)
    withdrawn = models.BooleanField(default=False)
    template_name = models.CharField(
        _('template name'),
        max_length=70,
        blank=True,
        help_text=_(
            'Example: “flatpages/contact_page.html”. If this isn’t provided, '
            'the system will use “flatpages/default.html”.'
        ),
    )
    registration_required = models.BooleanField(
        _('registration required'),
        help_text=_(
            "If this is checked, only logged-in users will be able to view the page."),
        default=False,
    )
    sites = models.ManyToManyField(Site, verbose_name=_('sites'))
    tags = TaggableManager(blank=True, through=CustomTaggedItem)
    history = HistoricalRecords()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("pages:page_detail", kwargs={"slug": self.slug})

    def get_index_view_url(self):
        content_type = ContentType.objects.get_for_model(
            self.__class__)
        return reverse("%s:index" % (content_type.app_label))
