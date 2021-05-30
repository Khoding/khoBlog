from comments.views import CommentUpdateView
from django.urls import path
from django_comments.feeds import LatestCommentFeed

app_name = 'comments'
urlpatterns = [
    path('<int:pk>/edit/', CommentUpdateView.as_view(), name='comments-edit'),
    path('rss/',
         LatestCommentFeed(), name='latest_comments_feed'),
]
