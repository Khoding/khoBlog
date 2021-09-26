from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .models import Post
from .serializers import PostSerializer, PostSerializerDetailV3, PostSerializerV3


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = Post.objects.filter(pub_date__lte=timezone.now(), withdrawn=False, is_removed=False)
        return queryset

    def get_serializer_class(self):
        if self.request.version == "v2":
            return PostSerializer
        if not self.detail:
            return PostSerializerV3
        return PostSerializerDetailV3

    lookup_field = "slug"
