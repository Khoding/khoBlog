# Application definition
from ..django import DEBUG
from ..third_party.django_debug_toolbar import ENABLE_DEBUG_TOOLBAR

INSTALLED_APPS = [
    "django_admin_index",
    "ordered_model",
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
    "django.contrib.humanize",
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
    "captcha",
    "storages",
    "robots",
    "taggit",
    "custom_taggit",
    "taggit_selectize",
    "simple_history",
    "rules",
    "widget_tweaks",
    "import_export",
    "compressor",
    "django_filters",
    "analytical",
    "django_markup",
    # Tailwind
    "django_browser_reload",
    "tailwind",
    "heroicons",
    "theme",
    # Django Packages Apps
    "django_comments_xtd",
    "django_comments",
    "comments",
    # APIs Apps
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
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
    "quotes",
    "lyrics",
]

if DEBUG and ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += [
        "debug_toolbar",
        "template_profiler_panel",
    ]
