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


class PostSerializerV3(serializers.ModelSerializer):
    # categories = CategorySerializer(many=True, read_only=True)
    # postcatslink_set = PostCatsLinkSerializer(many=True)

    class Meta:
        model = Post
        fields = ('pk', 'author_name', 'title', 'description',
                  'slug', 'created_date', 'modified_date', 'published_date',)
        prepopulated_fields = {'slug': ('title',)}
        lookup_field = 'slug'


class PostSerializerDetailV3(serializers.ModelSerializer):
    # categories = CategorySerializer(many=True, read_only=True)
    # postcatslink_set = PostCatsLinkSerializer(many=True)

    class Meta:
        model = Post
        fields = ('pk', 'author_name', 'title', 'formatted_markdown', 'description',
                  'slug', 'created_date', 'modified_date', 'published_date',)
        prepopulated_fields = {'slug': ('title',)}
        lookup_field = 'slug'
