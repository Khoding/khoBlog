from django.contrib.syndication.views import Feed
from django.utils import timezone

from .models import Post, Category, Comment


class LatestPostsFeed(Feed):
    title = 'Khodok\'s Blog'
    link = ''
    description = 'Latest posts of my blog.'

    def items(self):
        return Post.objects.filter(published_date__lte=timezone.now(), withdrawn=False).order_by('-published_date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.published_date

    def item_updateddate(self, item):
        return item.modified_date

    def item_author_name(self, item):
        return item.author

    def item_comments(self, item):
        return item.approved_comments()


class LatestPostsFeedByCategory(Feed):
    def get_object(self, request, slug):
        return Category.objects.get(slug=slug)

    def title(self, obj):
        return "Latest posts of %s" % obj.title

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return obj.description

    def items(self, obj):
        return Post.objects.filter(categories=obj, published_date__lte=timezone.now(), withdrawn=False).order_by(
            '-published_date')

    def item_description(self, item):
        return item.description

    def item_pubdate(self, item):
        return item.published_date

    def item_updateddate(self, item):
        return item.modified_date

    def item_author_name(self, item):
        return item.author

    def item_comments(self, item):
        return item.approved_comments()
