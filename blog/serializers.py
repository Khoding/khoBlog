from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post"""

    class Meta:
        """Meta"""

        model = Post
        fields = (
            "pk",
            "author_name",
            "title",
            "description",
            "slug",
            "created_date",
            "mod_date",
            "pub_date",
        )
        prepopulated_fields = {"slug": ("title",)}
        lookup_field = "slug"


class PostSerializerDetail(serializers.ModelSerializer):
    """Serializer for Post details"""

    class Meta:
        """Meta"""

        model = Post
        fields = (
            "pk",
            "author_name",
            "title",
            "formatted_markdown",
            "description",
            "slug",
            "created_date",
            "mod_date",
            "pub_date",
        )
        prepopulated_fields = {"slug": ("title",)}
        lookup_field = "slug"
