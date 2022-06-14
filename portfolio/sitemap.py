from django.contrib.sitemaps import Sitemap

from .models import Project


class ProjectSitemap(Sitemap):
    """ProjectSitemap Sitemap"""

    changefreq = "monthly"
    priority = 0.3
    protocol = "https"

    def items(self):
        return Project.objects.filter(deleted_at=None)

    def lastmod(self, obj):
        return obj.mod_date
