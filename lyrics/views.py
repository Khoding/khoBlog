from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView

from lyrics.forms import ArtistDeleteForm, SongDeleteForm

from .models import Artist, Song


class SongListView(ListView):
    """SongListView Class"""

    model = Song
    template_name = "lyrics/song_list.html"
    context_object_name = "songs"

    def get_queryset(self):
        """Get queryset"""
        return Song.objects.filter(deleted_at=None)

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Song List"
        context["description"] = "List of songs"
        return context


class SongDetailView(DetailView):
    """SongDetailView Class"""

    model = Song
    template_name = "lyrics/song_detail.html"

    def get_queryset(self):
        """Get the queryset for this view."""
        song = get_object_or_404(Song, slug=self.kwargs["slug"])
        if song.deleted_at:
            raise Http404
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["song"] = self.object
        context["title"] = self.object
        context["description"] = "Details for the song"
        return context


class SongDeleteView(UpdateView):
    """SongDeleteView

    View to delete a Song
    """

    model = Song
    template_name = "lyrics/song_confirm_delete.html"
    form_class = SongDeleteForm

    def get_queryset(self):
        """Get the queryset for this view."""
        if self.request.user.is_superuser:
            removing_song = get_object_or_404(Song, slug=self.kwargs["slug"])
            if self.get_form().is_valid():
                removing_song.soft_delete()
        else:
            raise PermissionDenied()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """get_context_data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Song"
        context["description"] = "Song deletion confirmation"
        return context


class ArtistListView(ListView):
    """ArtistListView Class"""

    model = Artist
    template_name = "lyrics/song_list.html"
    context_object_name = "songs"

    def get_queryset(self):
        """Get queryset"""
        return Artist.objects.filter(deleted_at=None)

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Artist List"
        context["description"] = "List of artists"
        return context


class ArtistDetailView(DetailView):
    """ArtistDetailView Class"""

    model = Artist
    template_name = "lyrics/artist_detail.html"

    def get_queryset(self):
        """Get the queryset for this view."""
        artist = get_object_or_404(Artist, slug=self.kwargs["slug"])
        if artist.deleted_at:
            raise Http404
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["artist"] = self.object
        context["title"] = self.object
        context["description"] = "Details for the artist"
        context["songs"] = Song.objects.filter(artist=self.object)
        return context


class ArtistDeleteView(UpdateView):
    """ArtistDeleteView

    View to delete a Artist
    """

    model = Artist
    template_name = "lyrics/song_confirm_delete.html"
    form_class = ArtistDeleteForm

    def get_queryset(self):
        """Get the queryset for this view."""
        if self.request.user.is_superuser:
            removing_artist = get_object_or_404(Artist, slug=self.kwargs["slug"])
            if self.get_form().is_valid():
                removing_artist.soft_delete()
        else:
            raise PermissionDenied()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """get_context_data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Artist"
        context["description"] = "Artist deletion confirmation"
        return context
