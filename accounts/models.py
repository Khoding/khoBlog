import auto_prefetch
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Role(auto_prefetch.Model):
    """
    The Role entries are managed by the system,
    automatically created via a Django data migration.
    """

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
        (BOT_OR_DUMMY, "Bot or Dummy"),
        (USER, "User"),
        (WORKPLACE, "Workplace"),
        (FRIEND, "Friend"),
        (MODERATOR, "Moderator"),
        (STAFF, "Staff"),
        (SPECIAL, "Special"),
        (ADMIN, "Admin"),
        (OWNER, "Website Owner"),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        """Return the name of the role"""
        return self.get_id_display()


class CustomUser(AbstractUser):
    """CustomUser Model Class"""

    email = models.EmailField()
    profile_pic = models.ImageField(
        null=True,
        blank=True,
        upload_to="images/profile/",
        verbose_name="Profile picture",
    )
    bio = models.TextField(blank=True, default="")
    slug = models.SlugField(
        blank=True,
        unique=True,
        default="",
        max_length=200,
        help_text="The slug is the direct link to your profile, it's auto generated based on your Username",
    )
    owner = models.BooleanField(default=False)
    welcome_message = models.CharField(
        max_length=42,
        blank=True,
        default="Hello",
        help_text="The message before your name when you are logged, by default 'Hello'",
    )
    roles = models.ManyToManyField(Role, blank=True, default="User")
    display_github = models.BooleanField(default=True, help_text="Show Github link on your profile page")
    secure_mode = models.BooleanField(default=False, help_text="Activate secure mode")

    def __str__(self):
        """String representation of CustomUser Model"""
        return self.username

    def save(self, *args, **kwargs):
        """Save method for CustomUser Model"""
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get absolute url for CustomUser Model"""
        return reverse("accounts:profile", kwargs={"slug": self.slug})

    def get_absolute_update_url(self):
        """Get absolute url for CustomUser Model"""
        return reverse("accounts:edit_profile", kwargs={"slug": self.slug})

    def get_absolute_admin_update_url(self):
        """Get the absolute admin update url"""
        return reverse("admin:accounts_customuser_change", kwargs={"object_id": self.pk})

    def get_absolute_update_secure_mode_status_url(self):
        """Get the absolute secure mode status update url"""
        return reverse("accounts:edit_secure_mode_status", kwargs={"slug": self.slug})

    def get_index_view_url(self):
        """Get the absolute index view url"""
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(f"{content_type.app_label}:profile", kwargs={"slug": self.slug})
