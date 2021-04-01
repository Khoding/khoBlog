from .models import Post
from django.urls import path
from django.urls.conf import include
from django.views.generic.dates import DateDetailView

from . import views
from .feeds import LatestPostsFeed, LatestPostsFeedByCategory, LatestCommentsFeed
from .views import AllSearchResultsListView, ApprovePostCommentUpdateView, CategoryCreateView, CategoryListView, CategorySearchResultsListView, CategoryUpdateView, CommentSearchResultsListView, PostArchiveIndexView, PostCommentCreateView, PostCommentUpdateView, PostCreateView, PostDayArchiveView, PostDeleteView, PostDraftListView, PostInCategoryListView, PostInSeriesListView, PostListView, PostMonthArchiveView, PostScheduledListView, PostSearchResultsListView, PostTodayArchiveView, PostUpdateView, PostDetailView, PostWeekArchiveView, PostWithdrawnListView, PostYearArchiveView, RandomSearchResultsListView, RemovePostCommentUpdateView, ReplyToCommentCreateView, SearchListView, SeriesCreateView, SeriesListView, SeriesUpdateView

post_action_extra_patterns = [
    path('', PostDetailView.as_view(), name='post_detail'),

    path('edit/', PostUpdateView.as_view(), name='post_edit'),
    path('publish/', views.post_publish, name='post_publish'),
    path('publish_withdrawn/',
         views.post_publish_withdrawn, name='post_publish_withdrawn'),
    path('delete/', PostDeleteView.as_view(), name='post_remove'),
]

category_action_extra_patterns = [
    path('', PostInCategoryListView.as_view(), name='post_category_list'),
    path('edit/',
         CategoryUpdateView.as_view(), name='category_edit'),
    path('rss/',
         LatestPostsFeedByCategory(), name='latest_category_post_feed'),
]

series_action_extra_patterns = [
    path('', PostInSeriesListView.as_view(), name='post_series_list'),
    path('edit/',
         SeriesUpdateView.as_view(), name='series_edit'),
]

category_extra_patterns = [
    path('', CategoryListView.as_view(),
         name='category_list'),
    path('add/', CategoryCreateView.as_view(), name='category_new'),
    path('<slug:slug>/', include(category_action_extra_patterns)),
]

series_extra_patterns = [
    path('', SeriesListView.as_view(),
         name='series_list'),
    path('add/', SeriesCreateView.as_view(), name='series_new'),
    path('<slug:slug>/', include(series_action_extra_patterns)),
]

post_comment_action_extra_patterns = [
    path('edit/', PostCommentUpdateView.as_view(),
         name='edit_post_comment'),
    path('reply/', ReplyToCommentCreateView.as_view(),
         name='add_reply_to_comment'),

    path('approve/', ApprovePostCommentUpdateView.as_view(), name='comment_approve'),
    path('remove/',
         RemovePostCommentUpdateView.as_view(), name='comment_remove'),
]

comment_extra_patterns = [
    path('', PostCommentCreateView.as_view(),
         name='add_comment_to_post'),
    path('<int:pk>/', include(post_comment_action_extra_patterns)),
]

post_extra_patterns = [
    path('add/', PostCreateView.as_view(), name='post_new'),
    # Goes to Post by redirecting through its ID or directly by slug respectively
    path('<int:pk>/', views.post_detail_through_id, name='post_detail'),
    path('<slug:slug>/', include(post_action_extra_patterns)),

    # Post Comments Related Patterns
    path('<int:pk_post>/comment/', include(comment_extra_patterns)),
]

search_extra_patterns = [
    path('', SearchListView.as_view(), name='search'),
    path('post/', PostSearchResultsListView.as_view(),
         name='post_search_results'),
    path('category/', CategorySearchResultsListView.as_view(),
         name='category_search_results'),
    path('comment/', CommentSearchResultsListView.as_view(),
         name='comment_search_results'),
    path('rnd/', RandomSearchResultsListView.as_view(),
         name='rnd_search_results'),
    path('all/', AllSearchResultsListView.as_view(),
         name='search_results'),
]

archive_extra_patterns = [
    path('',
         PostArchiveIndexView.as_view(),
         name="post_archive"),
    path('<int:year>/',
         PostYearArchiveView.as_view(), name='archive_year'),
    # Example: /2012/08/
    path('<int:year>/<int:month>/',
         PostMonthArchiveView.as_view(month_format='%m'),
         name="archive_month_numeric"),
    # Example: /2012/aug/
    path('<int:year>/<str:month>/',
         PostMonthArchiveView.as_view(),
         name="archive_month"),
    # Example: /2012/week/23/
    path('<int:year>/week/<int:week>/',
         PostWeekArchiveView.as_view(),
         name="archive_week"),
    # Example: /2012/Nov/10/
    path('<int:year>/<str:month>/<int:day>/',
         PostDayArchiveView.as_view(),
         name="archive_day"),
    path('<int:year>/<str:month>/<int:day>/<int:pk>/',
         DateDetailView.as_view(model=Post, date_field="published_date",
                                template_name="blog/archive_date_detail.html"),
         name="archive_date_detail"),
    path('today/',
         PostTodayArchiveView.as_view(),
         name="archive_today"),
]

app_name = 'blog'
urlpatterns = [
    # Lists
    path('', PostListView.as_view(), name='post_list'),
    path('latest/', views.redirect_to_latest, name='latest'),
    path('drafts/', PostDraftListView.as_view(), name='post_draft_list'),
    path('scheduled/', PostScheduledListView.as_view(),
         name='post_scheduled_list'),
    path('withdrawn/', PostWithdrawnListView.as_view(),
         name='post_withdrawn_list'),

    # Post Related Patterns
    path('post/', include(post_extra_patterns)),

    # Category Related Patterns
    path('category/', include(category_extra_patterns)),

    # Series Related Patterns
    path('series/', include(series_extra_patterns)),

    # Archives Related Patterns
    path('archives/', include(archive_extra_patterns)),

    # RSS Related Patterns
    path('latest/rss/', LatestPostsFeed(), name='latest_post_feed'),
    path('latest_comments/rss/',
         LatestCommentsFeed(), name='latest_comments_feed'),

    # Search Related Patterns
    path('search/', include(search_extra_patterns)),
]
