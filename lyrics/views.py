from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView

from lyrics.forms import SongDeleteForm

from .models import Song


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
        return context
