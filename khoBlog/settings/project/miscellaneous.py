from ..django import env


ROOT_URLCONF = "khoBlog.urls"
WSGI_APPLICATION = "khoBlog.wsgi.application"
HIDE_WEDNESDAY = env.bool("HIDE_WEDNESDAY")

INTERNAL_IPS = [
    "127.0.0.1",
]
