from django.urls import path
from django.urls.conf import include

from blog.views import CategoryDeleteView, SeriesDeleteView

from . import views
from .feeds import LatestPostsFeed, LatestPostsFeedByCategory
from .views import (
    AllSearchResultsListView,
    AllTagListView,
    ApprovePostCommentUpdateView,
    CategoryCreateView,
    CategoryListView,
    CategorySearchResultsListView,
    CategoryUpdateView,
    PostArchiveIndexView,
    PostCloneView,
    PostCommentCreateView,
    PostCommentUpdateView,
    PostCreateView,
    PostDateDetailView,
    PostDayArchiveView,
    PostDeleteView,
    PostDetailView,
    PostDraftListView,
    PostInCategoryListView,
    PostInSeriesListView,
    PostListView,
    PostMonthArchiveView,
    PostScheduledListView,
    PostSearchResultsListView,
    PostTodayArchiveView,
    PostUpdateView,
    PostWeekArchiveView,
    PostWithdrawnListView,
    PostWithTagListView,
    PostYearArchiveView,
    RandomSearchResultsListView,
    RemovePostCommentUpdateView,
    ReplyToCommentCreateView,
    SearchListView,
    SeriesCreateView,
    SeriesListView,
    SeriesUpdateView,
    TagsSearchResultsListView,
    TagUpdateView,
    WeblogTemplateView,
)

post_action_extra_patterns = [
    path("", PostDetailView.as_view(), name="post_detail"),
    path("edit/", PostUpdateView.as_view(), name="post_edit"),
    path("clone/", PostCloneView.as_view(), name="clone_post"),
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

tags_action_extra_patterns = [
    path("", PostWithTagListView.as_view(), name="post_tagged_with"),
    path("edit/", TagUpdateView.as_view(), name="tag_edit"),
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

tags_extra_patterns = [
    path("", AllTagListView.as_view(), name="tag_list"),
    path("<slug:slug>/", include(tags_action_extra_patterns)),
]

post_comment_action_extra_patterns = [
    path("edit/", PostCommentUpdateView.as_view(), name="edit_post_comment"),
    path("reply/", ReplyToCommentCreateView.as_view(), name="add_reply_to_comment"),
    path("approve/", ApprovePostCommentUpdateView.as_view(), name="comment_approve"),
    path("remove/", RemovePostCommentUpdateView.as_view(), name="comment_remove"),
]

comment_extra_patterns = [
    path("", PostCommentCreateView.as_view(), name="add_comment_to_post"),
    path("<int:pk>/", include(post_comment_action_extra_patterns)),
]

post_extra_patterns = [
    path("add/", PostCreateView.as_view(), name="create_post"),
    # Goes to Post by redirecting through its ID or directly by slug respectively
    path("<int:pk>/", views.post_detail_through_id, name="post_detail_through_id"),
    path("<int:pk>/", include(post_action_extra_patterns)),
    path("<slug:slug>/", include(post_action_extra_patterns)),
    # Post Comments Related Patterns
    path("<int:pk_post>/comment/", include(comment_extra_patterns)),
]

search_extra_patterns = [
    path("", SearchListView.as_view(), name="search"),
    path("post/", PostSearchResultsListView.as_view(), name="post_search_results"),
    path(
        "category/",
        CategorySearchResultsListView.as_view(),
        name="category_search_results",
    ),
    path("tag/", TagsSearchResultsListView.as_view(), name="tag_search_results"),
    path("rnd/", RandomSearchResultsListView.as_view(), name="rnd_search_results"),
    path("all/", AllSearchResultsListView.as_view(), name="search_results"),
]

archive_extra_patterns = [
    path("", PostArchiveIndexView.as_view(), name="post_archive"),
    path("<int:year>/", PostYearArchiveView.as_view(), name="archive_year"),
    # Example: /2012/08/
    path(
        "<int:year>/<int:month>/",
        PostMonthArchiveView.as_view(month_format="%m"),
        name="archive_month_numeric",
    ),
    # Example: /2012/aug/
    path("<int:year>/<str:month>/", PostMonthArchiveView.as_view(), name="archive_month"),
    # Example: /2012/week/23/
    path(
        "<int:year>/week/<int:week>/",
        PostWeekArchiveView.as_view(),
        name="archive_week",
    ),
    # Example: /2012/Nov/10/
    path(
        "<int:year>/<str:month>/<int:day>/",
        PostDayArchiveView.as_view(),
        name="archive_day",
    ),
    path(
        "<int:year>/<str:month>/<int:day>/<slug:slug>/",
        PostDateDetailView.as_view(),
        name="archive_date_detail",
    ),
    path("today/", PostTodayArchiveView.as_view(), name="archive_today"),
]

app_name = "blog"
urlpatterns = [
    # Lists
    path("", PostListView.as_view(), name="post_list"),
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
    # Tags Related Patterns
    path("tags/", include(tags_extra_patterns)),
    # Archives Related Patterns
    path("archives/", include(archive_extra_patterns)),
    # RSS Related Patterns
    path("latest/rss/", LatestPostsFeed(), name="latest_post_feed"),
    # Search Related Patterns
    path("search/", include(search_extra_patterns)),
]
