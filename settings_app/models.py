from django.db import models


class Settings(models.Model):
    THEME_CHOICES = [
        ('default', 'Default'),
        ('uglybanana', 'Funny Banana'),
        ('banana', 'Pretty Banana'),
        ('cherry', 'Hot Cherry'),
        ('sop', 'Shades Of Purple'),
        ('leaf', 'Smooth Leaf'),
        ('nightsky', 'Night Sky'),
    ]

    title = models.CharField(max_length=200)
    shown = models.BooleanField(default=False)
    side_menus = models.ManyToManyField(
        'settings_app.SideMenu', related_name='side_menus', blank=True)
    footers = models.ManyToManyField(
        'settings_app.Footer', related_name='footers', blank=True)
    default_theme = models.CharField(
        max_length=25, verbose_name="Theme", choices=THEME_CHOICES, default='default')

    class Meta:
        verbose_name_plural = "Settings Presets"

    def __str__(self):
        return self.title


class SideMenu(models.Model):
    title = models.CharField(max_length=200, blank=True)
    sub_title = models.CharField(max_length=200, blank=True)
    is_user_side_menu = models.BooleanField(default=False)
    is_post_list_side_menu = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Side Menus"

    def __str__(self):
        return self.title


class LinksSideMenu(models.Model):
    VISIBILITY_CHOICES = [
        ('D', 'default'),
        ('NP', 'needs_permission'),
        ('NS', 'needs_staff'),
        ('NA', 'needs_admin'),
    ]

    CLASSES_CHOICES = [
        ('PRI', 'primary'),
        ('SEC', 'secondary'),
        ('DAN', 'danger'),
        ('SUC', 'success'),
        ('WAR', 'warning'),
        ('INF', 'info'),
    ]

    title = models.CharField(max_length=200, blank=True)
    rel_url = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    links = models.ForeignKey(
        'settings_app.SideMenu', on_delete=models.CASCADE, related_name='side_menu_links')
    visibility = models.CharField(
        max_length=25, verbose_name="Visibility", choices=VISIBILITY_CHOICES, default='D')
    group = models.ForeignKey(
        'settings_app.LinksGroupSideMenu', on_delete=models.CASCADE, related_name='side_menu_links_group', blank=True, null=True)
    link_css_classes = models.CharField(
        max_length=25, verbose_name="Classes", choices=CLASSES_CHOICES, default='PRI')

    class Meta:
        verbose_name_plural = "Side Links"

    def __str__(self):
        return self.title

    def get_rel_url(self):
        return '/' + self.rel_url


class LinksGroupSideMenu(models.Model):
    title = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Side Links Group"

    def __str__(self):
        return self.title


class Footer(models.Model):
    title = models.CharField(max_length=200, blank=True)
    sub_title = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Footers"

    def __str__(self):
        return self.title


class LinksFooter(models.Model):
    title = models.CharField(max_length=200, blank=True)
    rel_url = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    links = models.ForeignKey(
        'settings_app.Footer', on_delete=models.CASCADE, related_name='footer_links')
    parent_css_classes = models.CharField(max_length=200, blank=True)
    link_css_classes = models.CharField(
        max_length=200, verbose_name="Classes", blank=True)
    child_img = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Footer Links"

    def __str__(self):
        return self.title

    def get_rel_url(self):
        return '/' + self.rel_url
