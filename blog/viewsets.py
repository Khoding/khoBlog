from rest_framework import viewsets
from .serializers import PostSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .models import Post

from django.utils import timezone


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Post.objects.filter(
        published_date__lte=timezone.now(), withdrawn=False, is_removed=False)
    serializer_class = PostSerializer
