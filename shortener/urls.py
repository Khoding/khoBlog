from django.urls import path

from shortener.views import short_redirect

app_name = "shortener"
urlpatterns = [
    path("<slug:slug>/", short_redirect, name="url_redirect"),
]
