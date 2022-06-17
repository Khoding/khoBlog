from rest_framework import serializers

from .models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    """Serializer for Resource"""

    class Meta:
        """Meta"""

        model = Resource
        fields = ("pk", "title", "description", "url", "withdrawn", "done")
