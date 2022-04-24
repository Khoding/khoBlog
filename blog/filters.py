from django import forms

import django_filters

from .models import Category, Post


class PostFilter(django_filters.FilterSet):
    """PostFilter

    A filter for Posts

    Args:
        django_filters ([type]): [description]

    Returns:
        [type]: [description]
    """

    title = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")
    body = django_filters.CharFilter(lookup_expr="icontains", widget=forms.Textarea)
    slug = django_filters.CharFilter(lookup_expr="icontains")
    categories = django_filters.ModelChoiceFilter(queryset=Category.objects.filter(withdrawn=False, is_removed=False))

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
