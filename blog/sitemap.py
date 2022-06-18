from django.contrib.sitemaps import Sitemap

from .models import Category, Post, Series


class PostSitemap(Sitemap):
    """PostSitemap Sitemap"""

    model = Post
    priority = 0.7
    protocol = "https"

    def items(self):
        """Items"""
        return self.model.objects.get_base_common_queryset()

    def lastmod(self, obj):
        """Lastmod"""
        return obj.pub_date


class CategorySitemap(Sitemap):
    """CategorySitemap Sitemap"""

    model = Category
    priority = 0.3
    protocol = "https"

    def items(self):
        """Items"""
        return self.model.objects.get_base_common_queryset()

    def lastmod(self, obj):
        """Lastmod"""
        return obj.mod_date


class SeriesSitemap(Sitemap):
    """SeriesSitemap Sitemap"""

    model = Series
    protocol = "https"

    def items(self):
        """Items"""
        return self.model.objects.get_base_common_queryset()

    def lastmod(self, obj):
        """Lastmod"""
        return obj.mod_date
