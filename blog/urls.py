from django.urls import path
from django.urls.conf import include

from blog.views import CategoryDeleteView, SeriesDeleteView

from . import views
from .feeds import LatestPostsFeed, LatestPostsFeedByCategory
from .views import (
    AllPostListView,
    CategoryCreateView,
    CategoryListView,
    CategoryUpdateView,
    PostCloneView,
    PostCreateView,
    PostDayArchiveView,
    PostDeleteView,
    PostDetailView,
    PostDraftListView,
    PostInCategoryListView,
    PostInSeriesListView,
    PostListView,
    PostScheduledListView,
    PostUpdateView,
    PostWithdrawnListView,
    SeriesCreateView,
    SeriesListView,
    SeriesUpdateView,
    WeblogTemplateView,
)

post_action_extra_patterns = [
    path("", PostDetailView.as_view(), name="post_detail"),
    path("edit/", PostUpdateView.as_view(), name="post_edit"),
    path("clone/", PostCloneView.as_view(), name="clone_post"),
    path("next/", views.post_next, name="post_next"),
    path("previous/", views.post_previous, name="post_previous"),
    path("publish/", views.post_publish, name="post_publish"),
    path(
        "publish_withdrawn/",
        views.post_publish_withdrawn,
        name="post_publish_withdrawn",
    ),
    path("needs_review/", views.post_needs_review, name="post_needs_review"),
    path("delete/", PostDeleteView.as_view(), name="post_remove"),
]

category_action_extra_patterns = [
    path("", PostInCategoryListView.as_view(), name="post_category_list"),
    path("edit/", CategoryUpdateView.as_view(), name="category_edit"),
    path("needs_review/", views.category_needs_review, name="category_needs_review"),
    path("delete/", CategoryDeleteView.as_view(), name="category_remove"),
    path("rss/", LatestPostsFeedByCategory(), name="latest_category_post_feed"),
]

series_action_extra_patterns = [
    path("", PostInSeriesListView.as_view(), name="post_series_list"),
    path("edit/", SeriesUpdateView.as_view(), name="series_edit"),
    path("needs_review/", views.series_needs_review, name="series_needs_review"),
    path("delete/", SeriesDeleteView.as_view(), name="series_remove"),
]

category_extra_patterns = [
    path("", CategoryListView.as_view(), name="category_list"),
    path("add/", CategoryCreateView.as_view(), name="create_category"),
    path("<slug:slug>/", include(category_action_extra_patterns)),
]

series_extra_patterns = [
    path("", SeriesListView.as_view(), name="series_list"),
    path("add/", SeriesCreateView.as_view(), name="create_series"),
    path("<slug:slug>/", include(series_action_extra_patterns)),
]


post_extra_patterns = [
    path("add/", PostCreateView.as_view(), name="create_post"),
    # Goes to Post by redirecting through its ID or directly by slug respectively
    path("<int:pk>/", views.post_detail_through_id, name="post_detail_through_id"),
    path("<int:pk>/", include(post_action_extra_patterns)),
    path("<slug:slug>/", include(post_action_extra_patterns)),
]


archive_extra_patterns = [
    # Example: /2012/Nov/10/
    path(
        "<int:year>/<str:month>/<int:day>/",
        PostDayArchiveView.as_view(),
        name="archive_day",
    ),
]

app_name = "blog"
urlpatterns = [
    # Lists
    path("", PostListView.as_view(), name="post_list"),
    path("all/", AllPostListView.as_view(), name="all_post_list"),
    path("latest/", views.redirect_to_latest, name="latest"),
    path("random/", views.redirect_to_random, name="random"),
    path("weblog/", WeblogTemplateView.as_view(), name="weblog"),
    path("drafts/", PostDraftListView.as_view(), name="post_draft_list"),
    path("scheduled/", PostScheduledListView.as_view(), name="post_scheduled_list"),
    path("withdrawn/", PostWithdrawnListView.as_view(), name="post_withdrawn_list"),
    # Post Related Patterns
    path("post/", include(post_extra_patterns)),
    # Category Related Patterns
    path("category/", include(category_extra_patterns)),
    # Series Related Patterns
    path("series/", include(series_extra_patterns)),
    # Archive Related Patterns
    path("archive/", include(archive_extra_patterns)),
    # RSS Related Patterns
    path("latest/rss/", LatestPostsFeed(), name="latest_post_feed"),
]
