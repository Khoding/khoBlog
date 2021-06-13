from learning_resources.views import ResourceViewSet
from django.urls.conf import include, path
from rest_framework import routers

from .viewsets import PostViewSet

router = routers.DefaultRouter()
router.register('post', PostViewSet, basename='post')
router.register('resource', ResourceViewSet, basename='resource')

urlpatterns = [
    path('', include(router.urls))
]
