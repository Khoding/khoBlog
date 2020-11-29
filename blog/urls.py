from django.urls import path

from . import views
from .feeds import LatestPostsFeed, LatestPostsFeedByCategory, LatestCommentsFeed
from .views import AddPostCommentView, EditPostCommentView, PostFutureListView, PostListView, PostDetailView, PostDraftListView, PostPrivateListView, AddPostView, EditPostView, \
    DeletePostView, AddCategoryView, PostListFromCategoryView, CategoryListView, EditCategoryView, SearchResultsView

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('drafts/', PostDraftListView.as_view(), name='post_draft_list'),
    path('future/', PostFutureListView.as_view(), name='post_future_list'),
    path('private/', PostPrivateListView.as_view(), name='post_private_list'),

    path('category/<slug:slug>/', PostListFromCategoryView.as_view(),
         name='post_category_list'),
    path('category_list/', CategoryListView.as_view(),
         name='category_list'),

    path('add_post/', AddPostView.as_view(), name='post_new'),
    path('add_category/', AddCategoryView.as_view(), name='category_new'),

    path('latest/', views.redirect_to_latest, name='latest'),

    path('post/<int:pk>/', views.PostDetailIDView, name='post_detail'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/edit/', EditPostView.as_view(), name='post_edit'),

    path('category/<slug:slug>/edit/',
         EditCategoryView.as_view(), name='category_edit'),

    path('post/<slug>/publish/', views.post_publish, name='post_publish'),
    path('post/<slug>/publish_private/',
         views.post_publish_private, name='post_publish_private'),
    path('post/<slug>/delete/', DeletePostView.as_view(), name='post_remove'),
    path('post/<int:pk>/comment/', AddPostCommentView.as_view(),
         name='add_comment_to_post'),
    path('comment/<int:pk>/edit', EditPostCommentView.as_view(),
         name='edit_post_comment'),

    path('comment/<int:pk>/approve/',
         views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/',
         views.comment_remove, name='comment_remove'),

    path('latest/rss/', LatestPostsFeed(), name='latest_post_feed'),
    path('category/<slug:slug>/rss/',
         LatestPostsFeedByCategory(), name='latest_category_post_feed'),
    path('latest_comments/rss/',
         LatestCommentsFeed(), name='latest_comments_feed'),

    path('search/', SearchResultsView.as_view(), name='search_results'),
]
