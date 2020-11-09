from khoBlogAPI.views import CategoryViewSet, CommentViewSet, PostViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('post', PostViewSet, basename='post')
router.register('category', CategoryViewSet, basename='category')
router.register('comment', CommentViewSet, basename='comment')

urlpatterns = router.urls
