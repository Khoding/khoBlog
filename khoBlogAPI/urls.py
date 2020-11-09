from khoBlogAPI.views import PostViewSet
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from khoBlogAPI import views

router = routers.DefaultRouter()
router.register(r'post', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
