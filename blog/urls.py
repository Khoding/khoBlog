from django.urls import path
from django.urls.conf import include

from . import views
from .feeds import LatestPostsFeed, LatestPostsFeedByCategory, LatestCommentsFeed
from .views import AddPostCommentView, EditPostCommentView, PostFutureListView, PostListView, PostDetailView, PostDraftListView, PostPrivateListView, AddPostView, EditPostView, \
    DeletePostView, AddCategoryView, PostListFromCategoryView, CategoryListView, EditCategoryView, RemovePostCommentView, SearchResultsView, AddReplyToComment

post_action_extra_patterns = [
    path('edit/', EditPostView.as_view(), name='post_edit'),
    path('publish/', views.post_publish, name='post_publish'),
    path('publish_private/',
         views.post_publish_private, name='post_publish_private'),
    path('delete/', DeletePostView.as_view(), name='post_remove'),
]

post_extra_patterns = [
    path('<int:pk>/', views.PostDetailIDView, name='post_detail'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/', include(post_action_extra_patterns)),
]

category_extra_patterns = [
    path('<slug:slug>/', PostListFromCategoryView.as_view(),
         name='post_category_list'),
    path('<slug:slug>/edit/',
         EditCategoryView.as_view(), name='category_edit'),
]

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('category_list/', CategoryListView.as_view(),
         name='category_list'),

    path('post/', include(post_extra_patterns)),

    path('category/', include(category_extra_patterns)),

    path('latest/', views.redirect_to_latest, name='latest'),
    path('drafts/', PostDraftListView.as_view(), name='post_draft_list'),
    path('future/', PostFutureListView.as_view(), name='post_future_list'),
    path('private/', PostPrivateListView.as_view(), name='post_private_list'),

    path('add_post/', AddPostView.as_view(), name='post_new'),
    path('add_category/', AddCategoryView.as_view(), name='category_new'),

    path('comment/<int:pk>/approve/',
         views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/',
         RemovePostCommentView.as_view(), name='comment_remove'),

    path('post/<int:pk>/comment/', AddPostCommentView.as_view(),
         name='add_comment_to_post'),
    path('post-<int:pk_post>/comment-<int:pk>/edit/', EditPostCommentView.as_view(),
         name='edit_post_comment'),
    path('post-<int:pk_post>/comment-<int:pk>/reply/', AddReplyToComment.as_view(),
         name='add_reply_to_comment'),


    path('latest/rss/', LatestPostsFeed(), name='latest_post_feed'),
    path('category/<slug:slug>/rss/',
         LatestPostsFeedByCategory(), name='latest_category_post_feed'),
    path('latest_comments/rss/',
         LatestCommentsFeed(), name='latest_comments_feed'),

    path('search/', SearchResultsView.as_view(), name='search_results'),
]
