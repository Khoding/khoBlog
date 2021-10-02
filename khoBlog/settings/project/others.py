from logging import debug
from ..django import DEBUG

ROOT_URLCONF = "khoBlog.urls"
WSGI_APPLICATION = "khoBlog.wsgi.application"

if not DEBUG:
    PREPEND_WWW = True
