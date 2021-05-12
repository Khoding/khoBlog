CACHE_MIDDLEWARE_ALIAS = 'default'  # which
CACHE_MIDDLEWARE_SECONDS = 600
# should be used if the cache is shared across multiple sites that use the same Django instance
CACHE_MIDDLEWARE_KEY_PREFIX = ''

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
        'OPTIONS': {
            'MAX_ENTRIES': 300,
        }
    },
}
