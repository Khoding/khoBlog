from django.urls.conf import include, path
from rest_framework import routers

from .viewsets import PostViewSet

router = routers.DefaultRouter()
router.register('post', PostViewSet)

urlpatterns = [
    path('', include(router.urls))
]
