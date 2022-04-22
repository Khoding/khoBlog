from django.urls import path
from django.urls.conf import include

from blog.views import PostWithTagListView

from .views import (
    TagListView,
    TagUpdateView,
)

tags_action_extra_patterns = [
    path("", PostWithTagListView.as_view(), name="post_tagged_with"),
    path("edit/", TagUpdateView.as_view(), name="tag_edit"),
]

app_name = "custom_taggit"
urlpatterns = [
    path("", TagListView.as_view(), name="tag_list"),
    path("<slug:slug>/", include(tags_action_extra_patterns)),
]
