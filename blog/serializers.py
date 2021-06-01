from rest_framework import serializers

from .models import Category, Post, PostCatsLink


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')


class PostCatsLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCatsLink
        fields = ('post', 'category', 'featured_cat')


class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    postcatslink_set = PostCatsLinkSerializer(many=True)

    class Meta:
        model = Post
        fields = ('title',
                  'description', 'body', 'categories', 'postcatslink_set',)
        prepopulated_fields = {'slug': ('title',)}
