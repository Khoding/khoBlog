from django.urls import path

from .views import home

app_name = 'api_read'
urlpatterns = [
    path('', home, name='index'),
]
