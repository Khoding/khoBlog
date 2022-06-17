from django.contrib.sitemaps import Sitemap

from .models import Page


class PageSitemap(Sitemap):
    """ProjectSitemap Sitemap"""

    changefreq = "monthly"
    priority = 0.6
    protocol = "https"

    def items(self):
        """Items"""
        return Page.objects.filter(withdrawn=False, deleted_at=None)

    def lastmod(self, obj):
        """Lastmod"""
        return obj.mod_date
