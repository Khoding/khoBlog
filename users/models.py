from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify


class CustomUser(AbstractUser):
    pass
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to="images/profile/")
    bio = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    owner = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)
