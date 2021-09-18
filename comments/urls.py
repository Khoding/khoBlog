from django.urls import path
from django_comments.feeds import LatestCommentFeed

from comments.views import CommentListView, CommentReplyView, CommentUpdateView

app_name = 'comments'
urlpatterns = [
    path('',
         CommentListView.as_view(), name='comments-list'),
    path('<int:pk>/edit/', CommentUpdateView.as_view(), name='comments-edit'),
    path('<int:pk>/reply/',
         CommentReplyView.as_view(), name='comments-reply'),
    path('rss/',
         LatestCommentFeed(), name='latest_comments_feed'),
]
