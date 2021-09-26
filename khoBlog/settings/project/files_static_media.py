from ..django import BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR + "/media"

STATIC_ROOT = BASE_DIR + "/static"

STATICFILES_DIRS = [
    (BASE_DIR + "/khoBlog/static"),
]
