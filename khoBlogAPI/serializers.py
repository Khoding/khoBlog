from rest_framework import serializers
from blog.models import Category, Post, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'categories',
                  'description', 'body', 'post_image')
        prepopulated_fields = {'slug': ('title',)}


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
