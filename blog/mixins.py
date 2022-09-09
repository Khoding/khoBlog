from .models import Category, Post, Series


class ListMixin:
    """Mixin for list views"""

    paginate_by = 20
    paginate_orphans = 5


class PostListMixin(ListMixin):
    """Mixin for posts"""

    model = Post
    template_name = "blog/lists/post_list.html"
    context_object_name = "posts"


class CategoryListMixin(ListMixin):
    """Mixin for categories"""

    model = Category
    template_name = "blog/lists/category_list.html"
    context_object_name = "category_list"


class SeriesListMixin(ListMixin):
    """Mixin for series"""

    model = Series
    template_name = "blog/lists/series_list.html"
    context_object_name = "series_list"
