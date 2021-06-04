from rest_framework import viewsets
from .serializers import PostSerializer

from .models import Post

from django.utils import timezone


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(
        published_date__lte=timezone.now(), withdrawn=False)
    serializer_class = PostSerializer
