import auto_prefetch
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Role(auto_prefetch.Model):
    '''
    The Role entries are managed by the system,
    automatically created via a Django data migration.
    '''
    BOT_OR_DUMMY = 1
    USER = 2
    WORKPLACE = 3
    FRIEND = 4
    MODERATOR = 5
    STAFF = 6
    SPECIAL = 7
    ADMIN = 8
    OWNER = 9
    ROLE_CHOICES = (
        (BOT_OR_DUMMY, 'Bot or Dummy'),
        (USER, 'User'),
        (WORKPLACE, 'Workplace'),
        (FRIEND, 'Friend'),
        (MODERATOR, 'Moderator'),
        (STAFF, 'Staff'),
        (SPECIAL, 'Special'),
        (ADMIN, 'Admin'),
        (OWNER, 'Website Owner'),
    )

    id = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


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
        null=True, blank=True, upload_to="images/profile/", verbose_name="Profile picture")
    bio = models.TextField(blank=True, default="")
    slug = models.SlugField(blank=True, unique=True,
                            default="", max_length=200, help_text="The slug is the direct link to your profile, it's auto generated based on your Username")
    owner = models.BooleanField(default=False)
    welcome_message = models.CharField(
        max_length=42, blank=True, default="Hello", help_text="The message before your name when you are logged, by default 'Hello'")
    default_theme = models.CharField(
        max_length=25, verbose_name="Theme", choices=THEME_CHOICES, default='default')
    roles = models.ManyToManyField(Role, blank=True, default="User")

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'slug': self.slug})

    def get_index_view_url(self):
        content_type = ContentType.objects.get_for_model(
            self.__class__)
        return reverse("%s:profile" % (content_type.app_label), kwargs={'slug': self.slug})
