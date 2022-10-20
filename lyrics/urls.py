from django.urls import path

from .views import SongListView, SongDetailView, SongDeleteView

app_name = "songs"
urlpatterns = [
    path("", SongListView.as_view(), name="song_list"),
    path("<slug:slug>/", SongDetailView.as_view(), name="song_detail"),
    path("<slug:slug>/delete/", SongDeleteView.as_view(), name="song_remove"),
]
