from django.contrib.sitemaps import Sitemap

from .models import Page


class PageSitemap(Sitemap):
    """ProjectSitemap Sitemap"""

    changefreq = "monthly"
    priority = 0.6
    protocol = "https"

    def items(self):
        return Page.objects.filter(withdrawn=False, is_removed=False)

    def lastmod(self, obj):
        return obj.mod_date
