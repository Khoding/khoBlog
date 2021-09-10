from django.contrib.syndication.views import Feed
from django.utils import timezone

from .models import Category, Post


class LatestPostsFeed(Feed):
    title = 'Khodok\'s Blog'
    link = ''
    description = 'Latest posts of my blog.'

    @staticmethod
    def items():
        return Post.objects.filter(published_date__lte=timezone.now(), withdrawn=False, is_removed=False)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()

    @staticmethod
    def item_pubdate(item):
        return item.published_date

    @staticmethod
    def item_updateddate(item):
        return item.modified_date

    @staticmethod
    def item_author_name(item):
        return item.author

    @staticmethod
    def item_comments(item):
        return item.approved_comments()


class LatestPostsFeedByCategory(Feed):
    def get_object(self, request, slug):
        return Category.objects.get(slug=slug)

    @staticmethod
    def title(obj):
        return "Latest posts of %s" % obj.title

    @staticmethod
    def link(obj):
        return obj.get_absolute_url()

    @staticmethod
    def description(obj):
        return obj.description

    @staticmethod
    def items(obj):
        return Post.objects.filter(categories=obj, published_date__lte=timezone.now(), withdrawn=False,
                                   is_removed=False).order_by(
            '-published_date')

    def item_description(self, item):
        return item.description

    @staticmethod
    def item_pubdate(item):
        return item.published_date

    @staticmethod
    def item_updateddate(item):
        return item.modified_date

    @staticmethod
    def item_author_name(item):
        return item.author

    @staticmethod
    def item_comments(item):
        return item.approved_comments()
