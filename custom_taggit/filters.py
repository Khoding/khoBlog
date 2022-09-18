from django_filters import CharFilter, FilterSet

from .models import CustomTag


class TagFilter(FilterSet):
    """TagFilter

    A filter for Tags
    """

    name = CharFilter(lookup_expr="icontains")

    class Meta:
        """Meta class for Post Filters"""

        model = CustomTag
        fields = [
            "name",
        ]

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(deleted_at=None)
