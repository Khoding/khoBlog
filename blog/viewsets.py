from rest_framework import viewsets
from .serializers import PostSerializer, PostSerializerV3
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .models import Post

from django.utils import timezone


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Post.objects.filter(
        published_date__lte=timezone.now(), withdrawn=False, is_removed=False)

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return PostSerializer
        else:
            return PostSerializerV3
    lookup_field = 'slug'
