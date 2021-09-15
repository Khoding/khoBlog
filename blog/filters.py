import django_filters
from django.db.models.query_utils import Q
from django.utils import timezone

from custom_taggit.models import CustomTag
from .models import Category, Post


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='contains')
    description = django_filters.CharFilter(lookup_expr='contains')
    body = django_filters.CharFilter(lookup_expr='contains')
    slug = django_filters.CharFilter(lookup_expr='contains')
    categories = django_filters.ModelChoiceFilter(
        queryset=Category.objects.filter(withdrawn=False, is_removed=False))
    tags = django_filters.ModelChoiceFilter(
        queryset=CustomTag.objects.filter(withdrawn=False))

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'body',
                  'slug', 'language', 'categories', 'tags', ]

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(is_removed=False)
