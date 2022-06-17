from django.contrib.sitemaps import Sitemap

from .models import Category, Post, Series


class PostSitemap(Sitemap):
    """PostSitemap Sitemap"""

    changefreq = "weekly"
    priority = 0.7
    protocol = "https"

    def items(self):
        """Items"""
        return Post.objects.get_base_common_queryset()

    def lastmod(self, obj):
        """Lastmod"""
        return obj.pub_date


class CategorySitemap(Sitemap):
    """CategorySitemap Sitemap"""

    changefreq = "monthly"
    priority = 0.5
    protocol = "https"

    def items(self):
        """Items"""
        return Category.objects.get_base_common_queryset()

    def lastmod(self, obj):
        """Lastmod"""
        return obj.mod_date


class SeriesSitemap(Sitemap):
    """SeriesSitemap Sitemap"""

    changefreq = "monthly"
    priority = 0.4
    protocol = "https"

    def items(self):
        """Items"""
        return Series.objects.get_base_common_queryset()

    def lastmod(self, obj):
        """Lastmod"""
        return obj.mod_date
