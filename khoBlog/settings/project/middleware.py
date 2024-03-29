from ..django import DEBUG
from ..third_party.django_debug_toolbar import ENABLE_DEBUG_TOOLBAR

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
]

if not DEBUG:
    MIDDLEWARE += [
        "django.middleware.cache.UpdateCacheMiddleware",
    ]

if DEBUG and ENABLE_DEBUG_TOOLBAR:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

MIDDLEWARE += [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

if not DEBUG:
    MIDDLEWARE += [
        "django.middleware.cache.FetchFromCacheMiddleware",
    ]

MIDDLEWARE += [
    "simple_history.middleware.HistoryRequestMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
]
