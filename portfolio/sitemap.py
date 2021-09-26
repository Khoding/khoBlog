from django.contrib.sitemaps import Sitemap

from .models import Project


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Project.objects.filter(is_removed=False)

    def lastmod(self, obj):
        return obj.modified_date
