# Application definition
from ..django import DEBUG
from ..third_party.django_debug_toolbar import ENABLE_DEBUG_TOOLBAR

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.redirects",
    "django.contrib.sitemaps",
    "django.contrib.flatpages",
    "django.forms",
    # Accounts
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.discord",
    "allauth.socialaccount.providers.github",
    "accounts",
    # Packages Apps
    "impostor",
    "markdownx",
    "django_editorjs_fields",
    "graphene_django",
    "captcha",
    "storages",
    "robots",
    "taggit",
    "custom_taggit",
    "taggit_selectize",
    "simple_history",
    "rules",
    "widget_tweaks",
    "sitetree",
    "import_export",
    "compressor",
    "django_filters",
    "analytical",
    "django_markup",
    "django_activeurl",
    "djversion",
    "tailwind",
    "theme",
    # Django Packages Apps
    "django_comments_xtd",
    "django_comments",
    "comments",
    # APIs Apps
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "khoBlogAPI",
    "learning_resources",
    # Website Settings App
    "settings_app",
    # Apps
    "blog",
    "portfolio",
    "pages",
    "polls",
    "todo",
    "shortener",
    "links",
    "reading_apis_app",
    "facts",
]

if DEBUG and ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += [
        "debug_toolbar",
        "template_profiler_panel",
    ]
