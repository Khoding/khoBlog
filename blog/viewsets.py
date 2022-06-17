from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .models import Post
from .serializers import PostSerializer, PostSerializerDetail


class PostViewSet(viewsets.ModelViewSet):
    """Viewset for post"""

    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = Post.objects.filter(pub_date__lte=timezone.now(), withdrawn=False, deleted_at=None)
        return queryset

    def get_serializer_class(self):
        if not self.detail:
            return PostSerializer
        return PostSerializerDetail

    lookup_field = "slug"
