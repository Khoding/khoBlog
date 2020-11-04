from blog.models import Post, Category, Comment
from rest_framework import viewsets
from .serializers import PostSerializer, CategorySerializer, CommentsSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = PostSerializer

