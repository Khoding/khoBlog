from django.contrib.contenttypes.views import shortcut
from django.urls import path
from django.urls.conf import re_path
from links.views import short_redirect

app_name = 'links'
urlpatterns = [
    path('<slug>/', short_redirect, name='url_redirect'),
    re_path(r'^cr/(\d+)/(.+)/$', shortcut, name='link-url-redirect'),
]
