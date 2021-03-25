from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify


class CustomUser(AbstractUser):
    THEME_CHOICES = [
        ('default', 'Default'),
        ('uglybanana', 'Funny Banana'),
        ('banana', 'Pretty Banana'),
        ('cherry', 'Hot Cherry'),
        ('sop', 'Shades Of Purple'),
        ('leaf', 'Smooth Leaf'),
        ('nightsky', 'Night Sky'),
    ]

    email = models.EmailField()
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to="images/profile/")
    bio = models.TextField(blank=True, default="")
    slug = models.SlugField(blank=True, unique=True,
                            default="", max_length=200)
    owner = models.BooleanField(default=False)
    welcome_message = models.CharField(
        max_length=42, blank=True, default="Hello", help_text="The message before your name when you are logged, by default 'Hello'")
    default_theme = models.CharField(
        max_length=25, verbose_name="Theme", choices=THEME_CHOICES, default='default')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'slug': self.slug})
