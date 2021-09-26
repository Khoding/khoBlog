from django.urls import path

from .views import return_the_api, return_the_api_detail

app_name = "api_read"
urlpatterns = [
    path("", return_the_api, name="index"),
    path("detail/", return_the_api_detail, name="api_read_detail"),
]
