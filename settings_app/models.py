import auto_prefetch
from django.db import models


class MenuFooter(auto_prefetch.Model):
    """Model for the menu footer"""

    title = models.CharField(max_length=200, blank=True)

    class Meta:
        """Meta"""

        verbose_name_plural = "Menu Footers"

    def __str__(self):
        return self.title


class MenuFooterLink(auto_prefetch.Model):
    """Model for the menu footer links"""

    VISIBILITY_CHOICES = [
        ("D", "default"),
        ("NP", "needs_permission"),
        ("NS", "needs_staff"),
        ("NA", "needs_admin"),
    ]

    title = models.CharField(max_length=200, blank=True)
    rel_url = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    visibility = models.CharField(
        max_length=25,
        verbose_name="Visibility",
        choices=VISIBILITY_CHOICES,
        default="D",
    )
    links = auto_prefetch.ForeignKey(
        "settings_app.MenuFooter", on_delete=models.CASCADE, related_name="menu_footer_links"
    )
    is_target_blank = models.BooleanField(default=False)

    class Meta:
        """Meta"""

        verbose_name_plural = "Menu Footer Links"

    def __str__(self):
        return self.title

    def get_rel_url(self):
        return "/" + self.rel_url
