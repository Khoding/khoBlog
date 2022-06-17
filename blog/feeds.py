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
        """Items"""
        return Post.objects.filter(pub_date__lte=timezone.now(), withdrawn=False, deleted_at=None)

    def item_title(self, item):
        """Item title"""
        return item.title

    def item_description(self, item):
        """Item description"""
        return item.description

    def item_link(self, item):
        """Item link"""
        return item.get_absolute_url()

    def item_pubdate(self, item):
        """Item pubdate"""
        return item.pub_date

    def item_updateddate(self, item):
        """Item updateddate"""
        return item.mod_date

    def item_author_name(self, item):
        """Item author name"""
        return item.author


class LatestPostsFeedByCategory(Feed):
    """LatestPostsFeedByCategory

    A feed for Post in a Category

    Args:
        Feed ([type]): [description]
    """

    def get_object(self, request, slug):
        """Get object"""
        return Category.objects.get(slug=slug)

    def title(self, obj):
        """Title"""
        return "Latest posts in %s" % obj.title

    def link(self, obj):
        """Link"""
        return obj.get_absolute_url()

    def description(self, obj):
        """Description"""
        return obj.description

    def items(self, obj):
        """Items"""
        return Post.objects.filter(
            categories=obj,
            pub_date__lte=timezone.now(),
            withdrawn=False,
            deleted_at=None,
        ).order_by("-pub_date")

    def item_description(self, item):
        """Item description"""
        return item.description

    def item_pubdate(self, item):
        """Item pubdate"""
        return item.pub_date

    def item_updateddate(self, item):
        """Item updateddate"""
        return item.mod_date

    def item_author_name(self, item):
        """Item author name"""
        return item.author
