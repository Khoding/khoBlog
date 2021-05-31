from django.shortcuts import render
from rest_framework import viewsets
from ..serializers import CategorySerializer, PostCatsLinkSerializer, PostSerializer

from ..models import Post, Category, Series

from django.utils import timezone


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(
        published_date__lte=timezone.now(), withdrawn=False).order_by('-published_date')
    serializer_class = PostSerializer
