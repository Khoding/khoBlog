from ..django import DEBUG

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
]

if not DEBUG:
    MIDDLEWARE += [
        'django.middleware.cache.UpdateCacheMiddleware',
    ]

MIDDLEWARE += [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
]

if not DEBUG:
    MIDDLEWARE += [
        'django.middleware.cache.FetchFromCacheMiddleware',
    ]

MIDDLEWARE += [
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]
