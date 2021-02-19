from django.urls import path
from django.urls.conf import include

from . import views
from .feeds import LatestPostsFeed, LatestPostsFeedByCategory, LatestCommentsFeed
from .views import AddPostCommentView, EditPostCommentView, PostFutureListView, PostListView, PostDetailView, PostDraftListView, PostWithdrawnListView, AddPostView, EditPostView, \
    DeletePostView, AddCategoryView, PostListFromCategoryView, CategoryListView, EditCategoryView, ApprovePostCommentView, RemovePostCommentView, SearchResultsView, AddReplyToComment

post_action_extra_patterns = [
    path('', PostDetailView.as_view(), name='post_detail'),

    path('edit/', EditPostView.as_view(), name='post_edit'),
    path('publish/', views.post_publish, name='post_publish'),
    path('publish_withdrawn/',
         views.post_publish_withdrawn, name='post_publish_withdrawn'),
    path('delete/', DeletePostView.as_view(), name='post_remove'),
]

category_extra_patterns = [
    path('', PostListFromCategoryView.as_view(),
         name='post_category_list'),
    path('edit/',
         EditCategoryView.as_view(), name='category_edit'),
    path('rss/',
         LatestPostsFeedByCategory(), name='latest_category_post_feed'),
]

post_comment_action_extra_patterns = [
    path('edit/', EditPostCommentView.as_view(),
         name='edit_post_comment'),
    path('reply/', AddReplyToComment.as_view(),
         name='add_reply_to_comment'),

    path('approve/', ApprovePostCommentView.as_view(), name='comment_approve'),
    path('remove/',
         RemovePostCommentView.as_view(), name='comment_remove'),
]

comment_extra_patterns = [
    path('', AddPostCommentView.as_view(),
         name='add_comment_to_post'),
    path('<int:pk_comment>/', include(post_comment_action_extra_patterns)),
]

post_extra_patterns = [
    # Goes to Post by redirecting through its ID or directly by slug respectively
    path('<int:pk>/', views.post_detail_through_id, name='post_detail'),
    path('<slug:slug>/', include(post_action_extra_patterns)),

    # Post Comments Related Links
    path('<int:pk>/comment/', include(comment_extra_patterns)),
]

app_name = 'blog'
urlpatterns = [
    # Lists
    path('', PostListView.as_view(), name='post_list'),
    path('latest/', views.redirect_to_latest, name='latest'),
    path('drafts/', PostDraftListView.as_view(), name='post_draft_list'),
    path('future/', PostFutureListView.as_view(), name='post_future_list'),
    path('withdrawn/', PostWithdrawnListView.as_view(),
         name='post_withdrawn_list'),

    # Post Related Links
    path('post/', include(post_extra_patterns)),
    path('add_post/', AddPostView.as_view(), name='post_new'),

    # Category Related Links
    path('category/<slug:slug>/', include(category_extra_patterns)),
    path('category_list/', CategoryListView.as_view(),
         name='category_list'),
    path('add_category/', AddCategoryView.as_view(), name='category_new'),

    # RSS Related Links
    path('latest/rss/', LatestPostsFeed(), name='latest_post_feed'),
    path('latest_comments/rss/',
         LatestCommentsFeed(), name='latest_comments_feed'),

    # Search Related Links
    path('search/', SearchResultsView.as_view(), name='search_results'),
]
