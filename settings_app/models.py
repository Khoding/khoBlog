from django.db import models


class Settings(models.Model):
    name = models.CharField(max_length=200)
    shown = models.BooleanField(default=False)
    user = models.ForeignKey(
        'settings_app.UserArea', on_delete=models.CASCADE, related_name='users_area')
    side_menus = models.ManyToManyField(
        'settings_app.SideMenu', related_name='side_menus', blank=True)

    class Meta:
        verbose_name_plural = "Settings Presets"

    def __str__(self):
        return self.name


class UserArea(models.Model):
    title = models.CharField(max_length=200)
    area_visible = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Users Area"

    def __str__(self):
        return self.title


class SideMenu(models.Model):
    title = models.CharField(max_length=200, blank=True)
    sub_title = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Side Menus"

    def __str__(self):
        return self.title


class LinksSideMenu(models.Model):
    VISIBILITY_CHOICES = [
        ('D', 'default'),
        ('NP', 'needs_permission'),
        ('NA', 'needs_admin'),
    ]

    name = models.CharField(max_length=200, blank=True)
    rel_url = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    links = models.ForeignKey(
        'settings_app.SideMenu', on_delete=models.CASCADE, related_name='side_menu_links')
    visibility = models.CharField(
        max_length=25, verbose_name="Visibility", choices=VISIBILITY_CHOICES, default='D')
    group = models.ForeignKey(
        'settings_app.LinksGroupSideMenu', on_delete=models.CASCADE, related_name='side_menu_links_group', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Side Links"

    def __str__(self):
        return self.name


class LinksGroupSideMenu(models.Model):
    name = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Side Links Group"

    def __str__(self):
        return self.name
