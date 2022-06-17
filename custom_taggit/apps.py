from django.apps import AppConfig


class CustomTaggitConfig(AppConfig):
    """Config for custom_taggit app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "custom_taggit"
