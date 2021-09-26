"""
Dev URLs.
DOC : https://docs.djangoproject.com/en/stable/topics/http/urls/
"""

from django.urls import path

from .dev_views import Error400View, Error403View, Error404View, Error500View
from ..settings import DEBUG

app_name = "dev"

if DEBUG:
    urlpatterns = [
        path("400/", Error400View.as_view(), name="400"),
        path("403/", Error403View.as_view(), name="403"),
        path("404/", Error404View.as_view(), name="404"),
        path("500/", Error500View.as_view(), name="500"),
    ]
else:
    urlpatterns = []
