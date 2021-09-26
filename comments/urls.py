from django.urls import path
from django_comments.feeds import LatestCommentFeed

app_name = "comments"
urlpatterns = [
    path("rss/", LatestCommentFeed(), name="latest_comments_feed"),
]
