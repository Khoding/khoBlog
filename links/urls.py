from django.urls import path
from links.views import short_redirect

app_name = 'links'
urlpatterns = [
    path('<slug>/', short_redirect, name='url_redirect'),
]
