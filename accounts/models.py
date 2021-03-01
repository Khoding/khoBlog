from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify


class CustomUser(AbstractUser):
    email = models.EmailField()
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to="images/profile/")
    bio = models.TextField(default="", blank=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    owner = models.BooleanField(default=False)
    welcome_message = models.CharField(
        max_length=42, blank=True, default="Hello", help_text="The message before your name when you are logged, by default 'Hello'")

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)
