from django.contrib.sitemaps import Sitemap

from .models import Category, Post, Series


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Post.objects.get_base_common_queryset()

    def lastmod(self, obj):
        return obj.pub_date


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.4
    protocol = 'https'

    def items(self):
        return Category.objects.get_base_common_queryset()

    def lastmod(self, obj):
        return obj.modified_date


class SeriesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.4
    protocol = 'https'

    def items(self):
        return Series.objects.get_base_common_queryset()

    def lastmod(self, obj):
        return obj.modified_date
