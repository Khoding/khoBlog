from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
import auto_prefetch

from django.template.defaultfilters import slugify

from graphql import GraphQLError


class URL(auto_prefetch.Model):
    title = models.CharField(max_length=200, unique=True)
    full_url = models.URLField(unique=True)
    slug = models.SlugField(unique=True, default="", max_length=200)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        validate = URLValidator()
        try:
            validate(self.full_url)
        except ValidationError as e:
            raise GraphQLError('invalid url')

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shortener:url_redirect", kwargs={"slug": self.slug})

    def clicked(self):
        self.clicks += 1
        self.save()
