from learning_resources.views import ResourceViewSet
from rest_framework import routers

from khoBlogAPI.views import CategoryViewSet, CommentViewSet, PostViewSet

router = routers.DefaultRouter()
router.register('post', PostViewSet, basename='post')
router.register('category', CategoryViewSet, basename='category')
router.register('comment', CommentViewSet, basename='comment')
router.register('resource', ResourceViewSet, basename='resource')

urlpatterns = router.urls
