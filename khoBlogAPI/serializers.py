from rest_framework import serializers
from blog.models import Category, Post, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PostSerializer(serializers.Serializer):
    class Meta:
        model = Post
        fields = ('title', 'categories',
                  'description', 'body', 'post_image')

    def create(self, validated_data):
        return Post(**validated_data)

    def update(self, instance, validated_data):
        instance.save(owner=instance.user)
        return instance


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
