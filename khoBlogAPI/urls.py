from django.conf.urls import url, include
from rest_framework import routers
from khoBlogAPI import views

router = routers.DefaultRouter()
router.register(r'post', views.PostViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]