from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

import auto_prefetch
from simple_history.models import HistoricalRecords


class BaseSongAbstractModel(auto_prefetch.Model):
    """BaseSongAbstractModel Model Class"""

    slug = models.SlugField(unique=True, default="", max_length=200, help_text="Song slug")
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta(auto_prefetch.Model.Meta):
        """Meta"""

        abstract = True

    # override the __str__ method to return the title of the song
    def __str__(self):
        """Return the title of the song"""
        return self.title


class Song(BaseSongAbstractModel):
    """Songs Model Class"""

    # choices of hosts
    HOST_CHOICES = (
        ("youtube", "YouTube"),
        ("youtube_music", "YouTube Music"),
        ("spotify", "Spotify"),
        ("google_play_music", "Google Play Music"),
        ("other", "Other"),
    )

    title = models.CharField(max_length=200, help_text="Song title")
    lyrics = models.TextField(help_text="Song lyrics")
    url_to_media = models.URLField()
    host = models.CharField(choices=HOST_CHOICES, max_length=200, default="spotify", help_text="Song host")
    deleted_at = models.DateTimeField(blank=True, null=True, help_text="Deletion date for soft delete")

    history = HistoricalRecords()

    class Meta(BaseSongAbstractModel.Meta):
        """Meta"""

    def save(self, *args, **kwargs):
        """Save"""
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get absolute url"""
        return reverse("songs:song_detail", kwargs={"slug": self.slug})

    def get_absolute_admin_update_url(self):
        """Get the admin update url for this song"""
        return reverse("admin:lyrics_song_change", kwargs={"object_id": self.pk})

    def get_absolute_delete_url(self):
        """Get the delete url for this song"""
        return reverse("songs:song_remove", kwargs={"slug": self.slug})

    def soft_delete(self):
        """Soft delete Category"""
        self.deleted_at = timezone.now()
        self.save()
