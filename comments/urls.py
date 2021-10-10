from django.urls import path

from django_comments.feeds import LatestCommentFeed

from comments.views import CommentListView

app_name = "comments"
urlpatterns = [
    path("", CommentListView.as_view(), name="comments-list"),
    path("rss/", LatestCommentFeed(), name="latest_comments_feed"),
]
