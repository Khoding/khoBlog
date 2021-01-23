from ..django import BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = (BASE_DIR + '/media')

STATIC_ROOT = (BASE_DIR + '/static')

STATICFILES_DIRS = [
    (BASE_DIR + '/khoBlog/static'),
]
