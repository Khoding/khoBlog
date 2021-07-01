from django.db.models.query_utils import Q
from django.utils import timezone
from .models import Category, Post
from custom_taggit.models import CustomTaggedItem
import django_filters


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    body = django_filters.CharFilter(lookup_expr='icontains')
    slug = django_filters.CharFilter(lookup_expr='icontains')
    categories = django_filters.ModelChoiceFilter(
        queryset=Category.objects.filter(withdrawn=False, is_removed=False))
    tags = django_filters.ModelChoiceFilter(
        queryset=CustomTaggedItem.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'body',
                  'slug', 'language', 'categories', 'tags', ]

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(Q(published_date__lte=timezone.now(), withdrawn=False, is_removed=False))
