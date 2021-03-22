from django.db import models


class Settings(models.Model):
    name = models.CharField(max_length=200)
    shown = models.BooleanField(default=False)
    about = models.ForeignKey(
        'settings_app.AboutArea', on_delete=models.CASCADE, related_name='about_area')
    user = models.ForeignKey(
        'settings_app.UserArea', on_delete=models.CASCADE, related_name='users_area')

    class Meta:
        verbose_name_plural = "Settings Presets"

    def __str__(self):
        return self.name


class AboutArea(models.Model):
    title = models.CharField(max_length=200)
    about = models.TextField()
    area_visible = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "About Area"

    def __str__(self):
        return self.about


class UserArea(models.Model):
    title = models.CharField(max_length=200)
    area_visible = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Users Area"

    def __str__(self):
        return self.title
