from django.contrib.syndication.views import Feed
from django.utils import timezone

from .models import Category, Post


class LatestPostsFeed(Feed):
    """LatestPostsFeed

    A feed for Post

    Args:
        Feed ([type]): [description]

    Returns:
        [type]: [description]
    """

    title = "Khodok's Blog"
    link = ""
    description = "Latest posts"

    @staticmethod
    def items():
        return Post.objects.filter(pub_date__lte=timezone.now(), withdrawn=False, is_removed=False)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()

    @staticmethod
    def item_pubdate(item):
        return item.pub_date

    @staticmethod
    def item_updateddate(item):
        return item.mod_date

    @staticmethod
    def item_author_name(item):
        return item.author


class LatestPostsFeedByCategory(Feed):
    """LatestPostsFeedByCategory

    A feed for Post in a Category

    Args:
        Feed ([type]): [description]
    """

    def get_object(self, request, slug):
        return Category.objects.get(slug=slug)

    @staticmethod
    def title(obj):
        return "Latest posts in %s" % obj.title

    @staticmethod
    def link(obj):
        return obj.get_absolute_url()

    @staticmethod
    def description(obj):
        return obj.description

    @staticmethod
    def items(obj):
        return Post.objects.filter(
            categories=obj,
            pub_date__lte=timezone.now(),
            withdrawn=False,
            is_removed=False,
        ).order_by("-pub_date")

    def item_description(self, item):
        return item.description

    @staticmethod
    def item_pubdate(item):
        return item.pub_date

    @staticmethod
    def item_updateddate(item):
        return item.mod_date

    @staticmethod
    def item_author_name(item):
        return item.author
