from django.urls import path
from django.urls.conf import include

from .views import (
    ProjectCreateView,
    ProjectDeleteView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
)

app_name = "portfolio"
project_extra_patterns = [
    path("", ProjectDetailView.as_view(), name="project_detail"),
    path("edit/", ProjectUpdateView.as_view(), name="project_edit"),
    path("delete/", ProjectDeleteView.as_view(), name="project_delete"),
]

urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
    path("add/", ProjectCreateView.as_view(), name="project_add"),
    path("<slug:slug>/", include(project_extra_patterns)),
]
