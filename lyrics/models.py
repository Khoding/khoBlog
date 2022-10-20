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
    release_date = models.DateField(blank=True, null=True)
    artist = models.ManyToManyField("lyrics.Artist", blank=True)
    featuring_artist = models.ManyToManyField("lyrics.Artist", blank=True, related_name="feat")
    genre = models.ManyToManyField("lyrics.Genre", blank=True)
    deleted_at = models.DateTimeField(blank=True, null=True, help_text="Deletion date for soft delete")

    history = HistoricalRecords()

    class Meta(BaseSongAbstractModel.Meta):
        """Meta"""

    # override the __str__ method to return the title of the quote
    def __str__(self):
        """Return the title of the quote"""
        return self.title

    def save(self, *args, **kwargs):
        """Save"""
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get absolute url"""
        return reverse("music:song_detail", kwargs={"slug": self.slug})

    def get_absolute_admin_update_url(self):
        """Get the admin update url for this song"""
        return reverse("admin:lyrics_song_change", kwargs={"object_id": self.pk})

    def get_absolute_delete_url(self):
        """Get the delete url for this song"""
        return reverse("music:song_remove", kwargs={"slug": self.slug})

    def soft_delete(self):
        """Soft delete Category"""
        self.deleted_at = timezone.now()
        self.save()


class Artist(BaseSongAbstractModel):
    """Artist Model Class"""

    name = models.CharField(max_length=255)
    about = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField("lyrics.Genre", blank=True)
    deleted_at = models.DateTimeField(blank=True, null=True, help_text="Deletion date for soft delete")

    history = HistoricalRecords()

    class Meta(BaseSongAbstractModel.Meta):
        """Meta"""

        pass

    # override the __str__ method to return the name of the artist
    def __str__(self):
        """__str__"""
        return self.name

    def save(self, *args, **kwargs):
        """Save"""
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get absolute url"""
        return reverse("music:artist_detail", kwargs={"slug": self.slug})

    def get_absolute_admin_update_url(self):
        """Get the admin update url for this artist"""
        return reverse("admin:lyrics_artist_change", kwargs={"object_id": self.pk})

    def get_absolute_delete_url(self):
        """Get the delete url for this artist"""
        return reverse("music:artist_remove", kwargs={"slug": self.slug})


class Genre(BaseSongAbstractModel):
    """Genre Model Class"""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True, help_text="Deletion date for soft delete")

    history = HistoricalRecords()

    class Meta(BaseSongAbstractModel.Meta):
        """Meta"""

        pass

    # override the __str__ method to return the title of the genre
    def __str__(self):
        """__str__"""
        return self.title

    def save(self, *args, **kwargs):
        """Save"""
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get absolute url"""
        return reverse("music:genre_detail", kwargs={"slug": self.slug})

    def get_absolute_admin_update_url(self):
        """Get the admin update url for this genre"""
        return reverse("admin:lyrics_genre_change", kwargs={"object_id": self.pk})

    def get_absolute_delete_url(self):
        """Get the delete url for this genre"""
        return reverse("music:genre_remove", kwargs={"slug": self.slug})
