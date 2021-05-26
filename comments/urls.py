from django.urls import path
from django_comments.feeds import LatestCommentFeed

urlpatterns = [
    path('rss/',
         LatestCommentFeed(), name='latest_comments_feed'),
]
