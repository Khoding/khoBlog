from taggit.models import Tag
import django_filters

from .models import Post


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    body = django_filters.CharFilter(lookup_expr='icontains')
    slug = django_filters.CharFilter(lookup_expr='icontains')
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'tags', 'title', 'description',
                  'slug', 'categories', 'body', ]
