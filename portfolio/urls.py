from django.urls import path
from django.urls.conf import include


from .views import (
    ProjectCreateView,
    ProjectDeleteView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
    SubProjectCreateView,
    SubProjectDeleteView,
    SubProjectDetailView,
    SubProjectListView,
    SubProjectUpdateView,
)

app_name = "portfolio"
sub_project_extra_actions_patterns = [
    path("", SubProjectDetailView.as_view(), name="sub_project_detail"),
    path("edit/", SubProjectUpdateView.as_view(), name="sub_project_edit"),
    path("delete/", SubProjectDeleteView.as_view(), name="sub_project_delete"),
]

sub_project_extra_patterns = [
    path("", SubProjectListView.as_view(), name="sub_project_list"),
    path("add/", SubProjectCreateView.as_view(), name="sub_project_add"),
    path("<slug:subproject_slug>/", include(sub_project_extra_actions_patterns)),
]

project_extra_patterns = [
    path("", ProjectDetailView.as_view(), name="project_detail"),
    path("sub/", include(sub_project_extra_patterns)),
    path("edit/", ProjectUpdateView.as_view(), name="project_edit"),
    path("delete/", ProjectDeleteView.as_view(), name="project_delete"),
]

urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
    path("add/", ProjectCreateView.as_view(), name="project_add"),
    path("<slug:slug>/", include(project_extra_patterns)),
]
