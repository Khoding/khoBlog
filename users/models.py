from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify


class CustomUser(AbstractUser):
    pass
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to="images/profile/")
    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)
