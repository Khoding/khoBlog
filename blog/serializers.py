from rest_framework import serializers

from .models import Category, Post, PostCatsLink


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')


class PostCatsLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCatsLink
        fields = ('__all__')


class PostSerializer(serializers.ModelSerializer):
    # categories = CategorySerializer(many=True, read_only=True)
    # postcatslink_set = PostCatsLinkSerializer(many=True)

    class Meta:
        model = Post
        fields = ('__all__')
        prepopulated_fields = {'slug': ('title',)}
        lookup_field = 'slug'
