from django.contrib.sitemaps import Sitemap

from .models import Project


class ProjectSitemap(Sitemap):
    """ProjectSitemap Sitemap"""

    changefreq = "monthly"
    priority = 0.3
    protocol = "https"

    def items(self):
        return Project.objects.filter(is_removed=False)

    @staticmethod
    def lastmod(obj):
        return obj.mod_date
