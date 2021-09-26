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

    def items(self):
        return Post.objects.filter(pub_date__lte=timezone.now(), withdrawn=False, is_removed=False)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.pub_date

    def item_updateddate(self, item):
        return item.modified_date

    def item_author_name(self, item):
        return item.author


class LatestPostsFeedByCategory(Feed):
    """LatestPostsFeedByCategory

    A feed for Post in a Category

    Args:
        Feed ([type]): [description]
    """

    def get_object(self, request, slug):
        return Category.objects.get(slug=slug)

    def title(self, obj):
        return "Latest posts in %s" % obj.title

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return obj.description

    def items(self, obj):
        return Post.objects.filter(
            categories=obj,
            pub_date__lte=timezone.now(),
            withdrawn=False,
            is_removed=False,
        ).order_by("-pub_date")

    def item_description(self, item):
        return item.description

    def item_pubdate(self, item):
        return item.pub_date

    def item_updateddate(self, item):
        return item.modified_date

    def item_author_name(self, item):
        return item.author
