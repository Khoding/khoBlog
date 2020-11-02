from django.contrib.syndication.views import Feed
from django.utils import timezone

from .models import Post, Category, Comment


class LatestPostsFeed(Feed):
    title = 'Khodok\'s Blog'
    link = ''
    description = 'Latest posts of my blog.'

    def items(self):
        return Post.objects.filter(published_date__lte=timezone.now(), private=False).order_by('-published_date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.published_date

    def item_author_name(self, item):
        return item.author


class LatestPostsFeedByCategory(Feed):
    title = 'Khodok\'s Blog'

    def get_object(self, request, slug):
        return Category.objects.get(slug=slug)

    def title(self, obj):
        return "Latest posts of %s" % obj.name

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return obj.description

    def items(self, obj):
        return Post.objects.filter(categories=obj, published_date__lte=timezone.now(), private=False).order_by(
            '-published_date')

    def item_description(self, item):
        return item.description

    def item_pubdate(self, item):
        return item.published_date

    def item_author_name(self, item):
        return item.author


class LatestCommentsFeed(Feed):
    title = 'Khodok\'s Blog'
    link = ''
    description = 'Comments to accept'

    def items(self):
        return Comment.objects.filter(approved_comment=False).order_by('-pk')

    def item_title(self, item):
        return item.author

    def item_description(self, item):
        return item.message

    def item_link(self, item):
        return item.post.get_absolute_url()

    def item_pubdate(self, item):
        return item.created_date
