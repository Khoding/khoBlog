from rest_framework import routers

from khoBlogAPI.views import CategoryViewSet, PostViewSet

router = routers.DefaultRouter()
router.register("post", PostViewSet, basename="post")
router.register("category", CategoryViewSet, basename="category")

urlpatterns = router.urls
