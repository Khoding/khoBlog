from django.urls import path
from django.urls.conf import include

from .views import (
    PageCreateView,
    PageDeleteView,
    PageDetailView,
    PageListView,
    PageUpdateView,
    kheee_page,
    about_page,
)

page_extra_patterns = [
    path("", PageDetailView.as_view(), name="page_detail"),
    path("edit/", PageUpdateView.as_view(), name="page_edit"),
    path("delete/", PageDeleteView.as_view(), name="page_delete"),
]

app_name = "pages"
urlpatterns = [
    path("", PageListView.as_view(), name="index"),
    path("add/", PageCreateView.as_view(), name="create_page"),
    path("<slug:slug>/", include(page_extra_patterns)),
    path("kheee/", kheee_page, name="kheee"),
    path("about/", about_page, name="about"),
]
