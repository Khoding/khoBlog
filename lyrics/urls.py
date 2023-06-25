from django.urls import path

from .views import SongListView, SongDetailView, SongDeleteView, ArtistListView, ArtistDetailView, ArtistDeleteView

app_name = "music"
urlpatterns = [
    path("song/", SongListView.as_view(), name="song_list"),
    path("song/<slug:artist_slug>/<slug:slug>/", SongDetailView.as_view(), name="song_detail"),
    path("song/<slug:slug>/delete/", SongDeleteView.as_view(), name="song_remove"),
    path("artist/", ArtistListView.as_view(), name="artist_list"),
    path("artist/<slug:slug>/", ArtistDetailView.as_view(), name="artist_detail"),
    path("artist/<slug:slug>/delete/", ArtistDeleteView.as_view(), name="artist_remove"),
]
