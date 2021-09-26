from django.urls import path
from django.urls.conf import include

from .views import (
    PageCreateView,
    PageDeleteView,
    PageDetailView,
    PageListView,
    PageUpdateView,
    kheee_special_case,
)

page_extra_patterns = [
    path("", PageDetailView.as_view(), name="page_detail"),
    path("edit/", PageUpdateView.as_view(), name="page_edit"),
    path("delete/", PageDeleteView.as_view(), name="page_delete"),
]

app_name = "pages"
urlpatterns = [
    path("", PageListView.as_view(), name="index"),
    path("add/", PageCreateView.as_view(), name="page_add"),
    path("<slug:slug>/", include(page_extra_patterns)),
    path("kheee/", kheee_special_case, name="kheee"),
]
