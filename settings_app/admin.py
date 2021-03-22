from django.contrib import admin
from .models import AboutArea, UserArea, Settings


class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'about', 'area_visible',)


class UsersAdmin(admin.ModelAdmin):
    list_display = ('title', 'area_visible',)


class PresetsSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'shown',)


admin.site.register(AboutArea, AboutAdmin)
admin.site.register(UserArea, UsersAdmin)
admin.site.register(Settings, PresetsSettingsAdmin)
