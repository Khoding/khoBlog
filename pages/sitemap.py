from django.contrib.sitemaps import Sitemap

from .models import Page


class PageSitemap(Sitemap):
    """ProjectSitemap Sitemap"""

    model = Page
    priority = 0.3
    protocol = "https"

    def items(self):
        """Items"""
        return self.model.objects.filter(withdrawn=False, deleted_at=None)

    def lastmod(self, obj):
        """Lastmod"""
        return obj.mod_date
