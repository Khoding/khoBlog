from django import forms

from django_filters import FilterSet, CharFilter, ModelChoiceFilter, OrderingFilter

from .models import Category, Post


class PostFilter(FilterSet):
    """PostFilter

    A filter for Posts

    Args:
        django_filters ([type]): [description]

    Returns:
        [type]: [description]
    """

    title = CharFilter(lookup_expr="icontains")
    description = CharFilter(lookup_expr="icontains")
    body = CharFilter(lookup_expr="icontains", widget=forms.Textarea)
    slug = CharFilter(lookup_expr="icontains")
    categories = ModelChoiceFilter(queryset=Category.objects.filter(withdrawn=False, is_removed=False))

    order_by = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("pk", "pk"),
            ("pub_date", "pub_date"),
            ("mod_date", "mod_date"),
            ("created_date", "created_date"),
        ),
        # labels do not need to retain order
        field_labels={
            "pk": "ID",
            "pub_date": "Publication Date",
            "-pub_date": "Publication Date (descending, default behaviour)",
            "mod_date": "Modification Date",
            "created_date": "Created Date",
        },
        label="Order by",
    )

    class Meta:
        """Meta class for Post Filters"""

        model = Post
        fields = [
            "title",
            "description",
            "body",
            "slug",
            "language",
            "categories",
        ]

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(is_removed=False)
