from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)
from django.views.generic.dates import (ArchiveIndexView, DateDetailView,
                                        DayArchiveView, MonthArchiveView,
                                        TodayArchiveView, WeekArchiveView,
                                        YearArchiveView)
from rules.contrib.views import AutoPermissionRequiredMixin

from blog.filters import PostFilter
from custom_taggit.models import CustomTag
from .forms import (ARPostCommentForm, CategoryCreateForm, CategoryDeleteForm,
                    CategoryEditForm, CommentForm, EditPostCommentForm,
                    PostCreateForm, PostDeleteForm, PostEditForm,
                    SeriesCreateForm, SeriesDeleteForm, SeriesEditForm)
from .models import Category, Comment, Post, PostContent, Series


def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass

    return wrapper


class PostListView(ListView):
    """PostListView List View

    The default List View for Posts

    Args:
        ListView (ListView): Lists elements

    Returns:
        posts: A list of posts
    """

    model = Post
    template_name = 'blog/lists/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        return self.model.objects.get_base_common_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Latest Posts'
        context['side_title'] = 'Post List'
        context['featured'] = self.model.objects.filter(
            featuring_state="F").get_without_removed()
        context['featured_big'] = self.model.objects.filter(
            featuring_state="FB").get_without_removed()
        return context


class WeblogTemplateView(TemplateView):
    """WeblogTemplateView TemplateView

    An alternative List View for Posts

    Args:
        TemplateView (TemplateView): A List View

    Returns:
        posts: A list of posts
    """

    template_name = 'blog/lists/weblog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Weblog'
        return context


class PostInCategoryListView(ListView):
    """PostInCategoryListView List View

    Lists all Posts in a particular Category

    Args:
        ListView (ListView): A list View

    Raises:
        PermissionDenied: If the currently logged in user doesn't have access to the requested Category

    Returns:
        posts: A list of posts
    """

    model = Post
    template_name = 'blog/lists/post_category_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, slug=self.kwargs['slug'])
        if not self.category.withdrawn or self.request.user.is_superuser:
            self.title = self.category.title
            self.description = self.category.description
        else:
            raise PermissionDenied
        return self.model.objects.get_common_queryset(self.request.user).filter(categories=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = self.category
        context['title'] = self.title
        context['description'] = self.description
        context['side_title'] = 'Post List'
        return context


class PostInSeriesListView(ListView):
    """PostInSeriesListView List View

    Lists all Posts in a particular Series

    Args:
        ListView (ListView): A list View

    Raises:
        PermissionDenied: If the currently logged in user doesn't have access to the requested Series

    Returns:
        posts: A list of posts
    """

    model = Post
    template_name = 'blog/lists/post_series_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        self.series = get_object_or_404(
            Series, slug=self.kwargs['slug'])
        if not self.series.withdrawn or self.request.user.is_superuser:
            self.title = self.series.title
            self.description = self.series.description
        else:
            raise PermissionDenied
        return self.model.objects.get_common_queryset(self.request.user).filter(series=self.series).order_by(
            'order_in_series')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['series'] = self.series
        context['title'] = self.series.title
        context['side_title'] = 'Post List'
        return context


class CategoryListView(ListView):
    """CategoryListView ListView

    A list of Categories

    Args:
        ListView ([type]): [description]

    Returns:
        category_list: A list of Categories
    """

    model = Category
    template_name = 'blog/lists/category_list.html'
    context_object_name = 'category_list'
    paginate_by = 21
    paginate_orphans = 5
    ordering = 'pk'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.get_without_removed()
        return self.model.objects.filter(
            withdrawn=False).get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Category List'
        context['search_url'] = reverse('blog:category_search_results')
        context['search_title'] = "Search in Categories"
        context['description'] = 'List of categories'
        return context


class SeriesListView(ListView):
    """SeriesListView ListView

    A list of Series

    Args:
        ListView ([type]): [description]

    Returns:
        series_list: A list of Series
    """

    model = Series
    template_name = 'blog/lists/series_list.html'
    context_object_name = 'series_list'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.get_without_removed()
        return self.model.objects.filter(withdrawn=False).get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Series List'
        return context


class PostDetailView(DetailView):
    """PostDetailView DetailView

    A view showing the Details of a Post

    Args:
        DetailView ([type]): [description]

    Raises:
        PermissionDenied: Post is removed
        PermissionDenied: User doesn't have access to requested Post

    Returns:
        [type]: [description]
    """

    model = Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        self.post = get_object_or_404(Post, slug=self.kwargs['slug'])
        self.post.clicked()
        if self.post.is_removed:
            raise PermissionDenied
        if self.request.user.is_superuser:
            self.series = self.model.objects.get_common_queryset(self.request.user).filter(
                series__isnull=False, series=self.post.series).order_by('order_in_series')
            self.title = self.post.title
            self.description = self.post.description
            if self.post.published_date:
                self.prev_post = (Post.objects
                                  .filter(published_date__lt=self.post.published_date, is_removed=False)
                                  .exclude(pk=self.post.pk)
                                  .order_by('-published_date')
                                  .first())
                self.next_post = (Post.objects
                                  .filter(published_date__gt=self.post.published_date, is_removed=False)
                                  .exclude(pk=self.post.pk)
                                  .order_by('published_date')
                                  .first())
            else:
                self.prev_post = (Post.objects
                                  .filter(created_date__lt=self.post.created_date, is_removed=False)
                                  .exclude(pk=self.post.pk)
                                  .order_by('-created_date')
                                  .first())
                self.next_post = (Post.objects
                                  .filter(created_date__gt=self.post.created_date, is_removed=False)
                                  .exclude(pk=self.post.pk)
                                  .order_by('created_date'))
        else:
            self.series = self.model.objects.get_common_queryset(self.request.user).filter(
                series__isnull=False, series=self.post.series).order_by('order_in_series')
            if self.post.withdrawn or not self.post.published_date or self.post.published_date >= timezone.now():
                raise PermissionDenied
            self.title = self.post.title
            self.description = self.post.description
            self.prev_post = (Post.objects
                              .filter(published_date__lt=self.post.published_date,
                                      published_date__lte=timezone.now(), withdrawn=False, is_removed=False)
                              .exclude(pk=self.post.pk)
                              .order_by('-published_date')
                              .first())
            self.next_post = (Post.objects
                              .filter(published_date__gt=self.post.published_date,
                                      published_date__lte=timezone.now(), withdrawn=False, is_removed=False)
                              .exclude(pk=self.post.pk)
                              .order_by('published_date')
                              .first())
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.get_base_common_queryset()
        context['series'] = self.series
        context['title'] = self.title
        context['body'] = PostContent.objects.filter(
            post_id=self.post.pk)
        context['description'] = self.description
        context['side_title'] = 'Post List'
        context['similar_posts'] = self.tags = self.post.tags.similar_objects()[
            :5]
        context['comment_next'] = self.post.get_absolute_url()
        context['next_post'] = self.next_post
        context['prev_post'] = self.prev_post
        return context


def redirect_to_latest(request):
    if request.user.is_superuser:
        latest = Post.objects.latest()
    else:
        latest = Post.objects.filter(
            published_date__lte=timezone.now(), withdrawn=False, is_removed=False).latest()
    return redirect(reverse('blog:post_detail', args=(latest.slug,)))


def post_detail_through_id(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return redirect(reverse('blog:post_detail', args=(post.slug,)))


@superuser_required()
class PostDraftListView(ListView):
    """PostDraftListView ListView

    Lists Draft Posts

    Args:
        ListView ([type]): [description]

    Returns:
        posts: A list of posts
    """

    model = Post
    template_name = 'blog/lists/post_draft_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        return self.model.objects.filter(published_date__isnull=True).order_by('-created_date').get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Drafts'
        return context


@superuser_required()
class PostScheduledListView(ListView):
    """PostScheduledListView ListView

    Lists Scheduled Posts

    Args:
        ListView ([type]): [description]

    Returns:
        posts: A list of posts
    """

    model = Post
    template_name = 'blog/lists/post_scheduled_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        return self.model.objects.filter(published_date__gte=timezone.now(), withdrawn=False).get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Scheduled'
        return context


@superuser_required()
class PostWithdrawnListView(ListView):
    """PostWithdrawnListView ListView

    Lists Withdrawn Posts

    Args:
        ListView ([type]): [description]

    Returns:
        posts: A list of posts
    """

    model = Post
    template_name = 'blog/lists/post_withdrawn_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        return self.model.objects.filter(withdrawn=True).get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Withdrawn'
        return context


class AllTagsListView(ListView):
    """AllTagsListView ListView

    Lists all Tags

    Args:
        ListView ([type]): [description]

    Returns:
        tags: A list of tags
    """

    model = CustomTag
    template_name = 'blog/lists/tags_list.html'
    context_object_name = 'tags'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(withdrawn=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tag List"
        context['description'] = "List of all tags"
        context['side_title'] = 'Tag List'
        context['search_url'] = reverse('blog:tag_search_results')
        context['search_title'] = "Search in Tags"
        return context


class PostWithTagListView(ListView):
    """PostWithTagListView ListView

    Lists all Posts tagged with a given Tag

    Args:
        ListView ([type]): [description]

    Returns:
        posts: A list of posts
    """

    model = Post
    template_name = 'blog/lists/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        self.tags = get_object_or_404(
            CustomTag, slug=self.kwargs['slug'])
        self.title = f'Tag: {self.tags.name}'
        self.description = f'Posts tagged with {self.tags.name}'
        return self.model.objects.get_common_queryset(self.request.user).filter(tags=self.tags)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = self.tags
        context['title'] = self.title
        context['description'] = self.description
        context['side_title'] = 'Post List'
        context['search_url'] = reverse('blog:tag_search_results')
        context['search_title'] = "Search in Tags"
        return context


@superuser_required()
class TagUpdateView(UpdateView):
    """TagUpdateView UpdateView

    A view to Update a Tag

    Args:
        UpdateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = CustomTag
    fields = ('__all__')
    template_name = "blog/category_edit.html"
    success_url = reverse_lazy('blog:tag_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by(
            '-pk')[:21]
        context['title'] = 'Edit Tag'
        context['side_title'] = 'Post List'
        return context


class PostCreateView(AutoPermissionRequiredMixin, CreateView):
    """PostCreateView CreateView

    A view to create a Post

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to create a Post
        CreateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Post
    form_class = PostCreateForm
    template_name = "blog/create_post.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.get_without_removed().order_by(
            '-pk')
        context['title'] = 'New Post'
        context['side_title'] = 'Post List'
        return context


class CategoryCreateView(AutoPermissionRequiredMixin, CreateView):
    """CategoryCreateView

    View to Create a Category

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to create a Category
        CreateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Category
    form_class = CategoryCreateForm
    template_name = "blog/create_category.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.get_without_removed().order_by(
            '-pk')
        context['title'] = 'New Category'
        context['side_title'] = 'Category List'
        return context


class SeriesCreateView(AutoPermissionRequiredMixin, CreateView):
    """SeriesCreateView

    A view to create a Series

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to create a Series
        CreateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Series
    form_class = SeriesCreateForm
    template_name = "blog/create_series.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.get_without_removed().order_by(
            '-pk')
        context['title'] = 'New Series'
        context['side_title'] = 'Series List'
        return context


class CategoryUpdateView(AutoPermissionRequiredMixin, UpdateView):
    """CategoryUpdateView

    View to update a Category

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to do that
        UpdateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Category
    form_class = CategoryEditForm
    template_name = "blog/category_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.get_without_removed().order_by(
            '-pk')
        context['title'] = 'Edit Category'
        context['side_title'] = 'Category List'
        return context


class CategoryDeleteView(AutoPermissionRequiredMixin, UpdateView):
    """CategoryDeleteView

    A view to delete a Category

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to do that
        UpdateView ([type]): [description]

    Raises:
        PermissionDenied: [description]

    Returns:
        [type]: [description]
    """

    model = Category
    template_name = 'blog/category_confirm_delete.html'
    form_class = CategoryDeleteForm
    success_url = reverse_lazy('blog:category_list')

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.category = get_object_or_404(
                Category, slug=self.kwargs['slug'])
            if self.get_form().is_valid():
                self.category.remove()
        else:
            raise PermissionDenied()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.get_without_removed().order_by(
            '-pk')
        context['title'] = 'Delete Category'
        context['side_title'] = 'Category List'
        return context


class SeriesUpdateView(AutoPermissionRequiredMixin, UpdateView):
    """SeriesUpdateView

    A view to update a Series

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to do that
        UpdateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Series
    form_class = SeriesEditForm
    template_name = "blog/series_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.get_without_removed().order_by(
            '-pk')
        context['title'] = 'Edit Series'
        context['side_title'] = 'Series List'
        return context


class SeriesDeleteView(AutoPermissionRequiredMixin, UpdateView):
    """SeriesDeleteView

    View to delete a Series

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to do that
        UpdateView ([type]): [description]

    Raises:
        PermissionDenied: [description]

    Returns:
        [type]: [description]
    """

    model = Series
    template_name = 'blog/series_confirm_delete.html'
    form_class = SeriesDeleteForm
    success_url = reverse_lazy('blog:series_list')

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.series = get_object_or_404(
                Series, slug=self.kwargs['slug'])
            if self.get_form().is_valid():
                self.series.remove()
        else:
            raise PermissionDenied()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.get_without_removed().order_by(
            '-pk')
        context['title'] = 'Delete Series'
        context['side_title'] = 'Series List'
        return context


class PostUpdateView(AutoPermissionRequiredMixin, UpdateView):
    """PostUpdateView

    View to update a Post

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to do that
        UpdateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Post
    form_class = PostEditForm
    template_name = "blog/post_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.get_without_removed().order_by(
            '-pk')
        context['title'] = 'Edit Post'
        context['side_title'] = 'Post List'
        return context


class PostCloneView(AutoPermissionRequiredMixin, CreateView):
    """PostCloneView Create View

    A view to clone a Post

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to do that
        CreateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Post
    template_name = 'blog/create_post.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        post = self.get_object()

        context = super().get_context_data(**kwargs)
        context['title'] = 'Clone Post'
        context['side_title'] = 'Post List'
        context['form'] = PostCreateForm(instance=post)
        return context


class PostDeleteView(AutoPermissionRequiredMixin, UpdateView):
    """PostDeleteView

    View to delete a Post

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to do that
        UpdateView ([type]): [description]

    Raises:
        PermissionDenied: [description]

    Returns:
        [type]: [description]
    """

    model = Post
    template_name = 'blog/post_confirm_delete.html'
    form_class = PostDeleteForm
    success_url = reverse_lazy('blog:post_list')

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.removing_post = get_object_or_404(
                Post, slug=self.kwargs['slug'])
            if self.get_form().is_valid():
                self.removing_post.remove()
        else:
            raise PermissionDenied()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.get_without_removed().order_by(
            '-pk')
        context['title'] = 'Delete Post'
        context['side_title'] = 'Post List'
        return context


class SearchListView(ListView):
    """SearchListView

    Search View

    Args:
        ListView ([type]): [description]

    Returns:
        [type]: [description]
    """

    template_name = 'blog/search.html'
    context_object_name = 'query'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        query = [[{'id': 1, 'title': 'Search in Posts', 'get_absolute_url': 'post/?q=', },
                  {'id': 2, 'title': 'Search in Categories',
                      'get_absolute_url': 'category/?q=', },
                  {'id': 3, 'title': 'Search in Tags',
                      'get_absolute_url': 'tag/?q=', },
                  {'id': 4, 'title': 'Search in Everything', 'get_absolute_url': 'all/?q='}, ]]
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search'
        context['search_url'] = reverse('blog:search_results')
        context['search_title'] = "Search in Everything"
        return context


class PostSearchResultsListView(ListView):
    """PostSearchResultsListView

    Search result list view

    Args:
        ListView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Post
    template_name = 'blog/lists/filter_list.html'
    context_object_name = 'filter'

    def get_queryset(self):
        if self.request.user.is_superuser:
            query = PostFilter(self.request.GET,
                               queryset=self.model.objects.all())
        else:
            query = PostFilter(self.request.GET,
                               queryset=self.model.objects.filter(
                                   Q(published_date__lte=timezone.now(), withdrawn=False)))
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search in Posts'
        context['search_url'] = reverse('blog:post_search_results')
        context['search_title'] = "Search in Posts"
        return context


class CategorySearchResultsListView(ListView):
    """CategorySearchResultsListView

    Category results listing view

    Args:
        ListView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Category
    template_name = 'blog/search.html'
    context_object_name = 'query'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is not None:
            if self.request.user.is_superuser:
                return self.model.objects.filter(
                    Q(title__contains=query) | Q(
                        description__contains=query),
                ).get_without_removed()
            return self.model.objects.filter(
                Q(title__contains=query) | Q(
                    description__contains=query),
            ).filter(~Q(withdrawn=True),
                     ).get_without_removed()
        if self.request.user.is_superuser:
            category = self.model.objects.get_without_removed()
            return category
        category = self.model.objects.filter(
            ~Q(withdrawn=True), ).get_without_removed()
        return category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search in Categories'
        context['search_url'] = reverse('blog:category_search_results')
        context['search_title'] = "Search in Categories"
        return context


class TagsSearchResultsListView(ListView):
    """TagsSearchResultsListView

    Tags search result listing view

    Args:
        ListView ([type]): [description]

    Returns:
        [type]: [description]
    """

    template_name = 'blog/search.html'
    context_object_name = 'query'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is not None:
            if not self.request.user.is_superuser:
                return CustomTag.objects.filter(
                    Q(name__contains=query, withdrawn=False)
                )
            return CustomTag.objects.filter(
                Q(name__contains=query)
            )
        if not self.request.user.is_superuser:
            tag = CustomTag.objects.filter(withdrawn=False)
        else:
            tag = CustomTag.objects.all()
        return tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search in Tags'
        context['search_url'] = reverse('blog:tag_search_results')
        context['search_title'] = "Search in Tags"
        return context


class RandomSearchResultsListView(ListView):
    """RandomSearchResultsListView

    Random search view

    Args:
        ListView ([type]): [description]

    Returns:
        [type]: [description]
    """

    template_name = 'blog/search.html'
    context_object_name = 'query'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Random Search'
        context['search_url'] = reverse('blog:rnd_search_results')
        context['search_title'] = "Have fun"
        return context


class AllSearchResultsListView(ListView):
    """AllSearchResultsListView

    Search everywhere results list view

    Args:
        ListView ([type]): [description]

    Returns:
        [type]: [description]
    """

    template_name = 'blog/search.html'
    context_object_name = 'query'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is not None:
            if self.request.user.is_superuser:
                post = Post.objects.filter(
                    Q(title__contains=query) | Q(
                        body__contains=query) | Q(description__contains=query),
                ).get_without_removed()
                category = Category.objects.filter(
                    Q(title__contains=query) | Q(
                        description__contains=query),
                ).get_without_removed()
                tag = CustomTag.objects.filter(
                    Q(name__contains=query)
                )
                return [post, category, tag]
            post = Post.objects.filter(
                Q(title__contains=query) | Q(
                    body__contains=query) | Q(description__contains=query),
            ).filter(~Q(published_date__gt=timezone.now()), ~Q(published_date__isnull=True), ~Q(withdrawn=True),
                     ).get_without_removed()
            category = Category.objects.filter(
                Q(title__contains=query) | Q(
                    description__contains=query),
            ).filter(~Q(withdrawn=True),
                     ).get_without_removed()
            tag = CustomTag.objects.filter(
                Q(name__contains=query)
            ).filter(~Q(withdrawn=True),
                     )
            return [post, category, tag]
        if self.request.user.is_superuser:
            post = Post.objects.get_without_removed()
            category = Category.objects.get_without_removed()
            tag = CustomTag.objects.all()
            return [post, category, tag]
        post = Post.objects.filter(~Q(published_date__gt=timezone.now()), ~Q(
            published_date__isnull=True), ~Q(withdrawn=True), ).get_without_removed()
        category = Category.objects.filter(
            ~Q(withdrawn=True), ).get_without_removed()
        tag = CustomTag.objects.filter(~Q(withdrawn=True),
                                       )
        return [post, category, tag]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search in Everything'
        context['search_url'] = reverse('blog:search_results')
        context['search_title'] = "Search in Everything"
        return context


@user_passes_test(lambda u: u.is_superuser)
def post_publish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.publish()
    return redirect('blog:post_detail', slug=slug)


@user_passes_test(lambda u: u.is_superuser)
def post_publish_withdrawn(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.withdrawn = True
    post.publish_withdrawn()
    return redirect('blog:post_detail', slug=slug)


@superuser_required()
class PostCommentCreateView(LoginRequiredMixin, CreateView):
    """PostCommentCreateView

    Create a comment

    Args:
        LoginRequiredMixin ([type]): [description]
        CreateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Comment
    form_class = CommentForm
    template_name = "blog/comments/add_comment_to_post.html"

    def form_valid(self, form):
        form.instance.author_logged = self.request.user
        form.instance.related_post_id = self.kwargs['pk_post']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(
            published_date__lte=timezone.now(), withdrawn=False)
        context['title'] = 'Add Comment'
        context['side_title'] = 'Post List'
        return context


@superuser_required()
class ReplyToCommentCreateView(LoginRequiredMixin, CreateView):
    """ReplyToCommentCreateView

    Reply to a comment

    Args:
        LoginRequiredMixin ([type]): [description]
        CreateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Comment
    form_class = CommentForm
    template_name = "blog/comments/add_comment_to_post.html"

    def form_valid(self, form):
        form.instance.author_logged = self.request.user
        form.instance.related_post_id = self.kwargs['pk_post']
        form.instance.comment_answer_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(
            published_date__lte=timezone.now(), withdrawn=False)
        context['title'] = 'Reply to Comment'
        context['side_title'] = 'Post List'
        return context


@superuser_required()
class PostCommentUpdateView(LoginRequiredMixin, UpdateView):
    """PostCommentUpdateView

    Update a comment

    Args:
        LoginRequiredMixin ([type]): [description]
        UpdateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Comment
    form_class = EditPostCommentForm
    template_name = 'blog/comments/edit_comment.html'

    def form_valid(self, form):
        form.instance.related_post_id = self.kwargs['pk_post']
        form.instance.comment_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(
            published_date__lte=timezone.now(), withdrawn=False)
        context['title'] = 'Edit Comment'
        context['side_title'] = 'Post List'
        return context


@superuser_required()
class ApprovePostCommentUpdateView(UpdateView):
    """ApprovePostCommentUpdateView

    Approve a comment

    Args:
        UpdateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Comment
    form_class = ARPostCommentForm
    template_name = 'blog/comments/approve_post_comment.html'

    def get_queryset(self):
        self.comment = get_object_or_404(
            Comment, pk=self.kwargs['pk'])
        self.comment.approve()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.get_without_removed().order_by('-pk')
        context['title'] = 'Approve Comment'
        context['side_title'] = 'Post List'
        return context


@superuser_required()
class RemovePostCommentUpdateView(UpdateView):
    """RemovePostCommentUpdateView

    Remove a comment

    Args:
        UpdateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Comment
    form_class = ARPostCommentForm
    template_name = 'blog/comments/remove_post_comment.html'

    def get_queryset(self):
        self.comment = get_object_or_404(
            Comment, pk=self.kwargs['pk'])
        self.comment.remove()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(
            published_date__lte=timezone.now(), withdrawn=False)
        context['title'] = 'Remove Comment'
        context['side_title'] = 'Post List'
        return context


class PostArchiveIndexView(ArchiveIndexView):
    """PostArchiveIndexView

    Archive view

    Args:
        ArchiveIndexView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Post
    template_name = 'blog/lists/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5
    allow_empty = True
    make_object_list = True
    date_field = "published_date"
    allow_future = True

    def get_queryset(self):
        return self.model.objects.get_common_queryset(self.request.user).get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Post archives'
        return context


class PostYearArchiveView(YearArchiveView):
    """PostYearArchiveView

    Archive by year

    Args:
        YearArchiveView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Post
    template_name = 'blog/lists/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5
    allow_empty = True
    make_object_list = True
    date_field = "published_date"
    allow_future = True

    def get_queryset(self):
        return self.model.objects.get_common_queryset(user=self.request.user).get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted in ' + str(self.get_year())
        return context


class PostMonthArchiveView(MonthArchiveView):
    """PostMonthArchiveView

    Archive by month

    Args:
        MonthArchiveView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Post
    template_name = 'blog/lists/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5
    allow_empty = True
    date_field = "published_date"
    allow_future = True

    def get_queryset(self):
        return self.model.objects.get_common_queryset(user=self.request.user).get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted in ' + \
                           str(self.get_month()) + \
                           ' of ' + str(self.get_year())
        return context


class PostWeekArchiveView(WeekArchiveView):
    """PostWeekArchiveView

    Archive by week

    Args:
        WeekArchiveView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Post
    template_name = 'blog/lists/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5
    date_field = 'published_date'
    week_format = '%W'
    allow_future = True

    def get_queryset(self):
        return self.model.objects.get_common_queryset(user=self.request.user).get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted during Week ' + \
                           str(self.get_week()) + ' of ' + str(self.get_year())
        return context


class PostDayArchiveView(DayArchiveView):
    """PostDayArchiveView

    Archive by day

    Args:
        DayArchiveView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Post
    template_name = 'blog/lists/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5
    date_field = 'published_date'
    allow_future = True

    def get_queryset(self):
        return self.model.objects.get_common_queryset(user=self.request.user).get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted the ' + \
                           str(self.get_day()) + ' ' + str(self.get_month()) + \
                           ' ' + str(self.get_year())
        context['archive'] = True
        context['g_day'] = f'{self.get_day()}'
        context['g_month'] = f'{self.get_month()}'
        context['g_year'] = f'{self.get_year()}'
        return context


class PostDateDetailView(DateDetailView):
    """PostDateDetailView

    Detail for Archive by day

    Args:
        DateDetailView ([type]): [description]

    Raises:
        PermissionDenied: [description]
        PermissionDenied: [description]

    Returns:
        [type]: [description]
    """

    model = Post
    template_name = 'blog/archive_date_detail.html'
    date_field = "published_date"

    def get_queryset(self):
        self.post = get_object_or_404(Post, slug=self.kwargs['slug'])
        self.post.clicked()
        if self.post.is_removed:
            raise PermissionDenied
        if self.request.user.is_superuser:
            self.series = self.model.objects.get_common_queryset(self.request.user).filter(
                series__isnull=False, series=self.post.series).order_by('order_in_series')
            self.title = self.post.title
            self.description = self.post.description
            if self.post.published_date:
                self.prev_post = (Post.objects
                                  .filter(published_date__lt=self.post.published_date, is_removed=False)
                                  .exclude(pk=self.post.pk)
                                  .order_by('-published_date')
                                  .first())
                self.next_post = (Post.objects
                                  .filter(published_date__gt=self.post.published_date, is_removed=False)
                                  .exclude(pk=self.post.pk)
                                  .order_by('published_date')
                                  .first())
            else:
                self.prev_post = (Post.objects
                                  .filter(created_date__lt=self.post.created_date, is_removed=False)
                                  .exclude(pk=self.post.pk)
                                  .order_by('-created_date')
                                  .first())
                self.next_post = (Post.objects
                                  .filter(created_date__gt=self.post.created_date, is_removed=False)
                                  .exclude(pk=self.post.pk)
                                  .order_by('created_date'))
        else:
            self.series = self.model.objects.get_common_queryset(self.request.user).filter(
                series__isnull=False, series=self.post.series).order_by('order_in_series')
            if self.post.withdrawn or not self.post.published_date or self.post.published_date >= timezone.now():
                raise PermissionDenied
            self.title = self.post.title
            self.description = self.post.description
            self.prev_post = (Post.objects
                              .filter(published_date__lt=self.post.published_date,
                                      published_date__lte=timezone.now(), withdrawn=False, is_removed=False)
                              .exclude(pk=self.post.pk)
                              .order_by('-published_date')
                              .first())
            self.next_post = (Post.objects
                              .filter(published_date__gt=self.post.published_date,
                                      published_date__lte=timezone.now(), withdrawn=False, is_removed=False)
                              .exclude(pk=self.post.pk)
                              .order_by('published_date')
                              .first())
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted the ' + \
                           str(self.get_day()) + ' ' + str(self.get_month()) + \
                           ' ' + str(self.get_year())
        context['posts'] = self.model.objects.get_common_queryset(
            self.request.user)
        context['series'] = self.series
        context['body'] = PostContent.objects.filter(
            post_id=self.post.pk)
        context['description'] = self.description
        context['side_title'] = 'Post List'
        context['similar_posts'] = self.tags = self.post.tags.similar_objects()[
            :5]
        context['next_post'] = self.next_post
        context['prev_post'] = self.prev_post
        return context


class PostTodayArchiveView(TodayArchiveView):
    """PostTodayArchiveView

    Archive for today

    Args:
        TodayArchiveView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Post
    template_name = 'blog/lists/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5
    allow_empty = True
    date_field = "published_date"
    allow_future = True

    def get_queryset(self):
        return self.model.objects.get_common_queryset(user=self.request.user).get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted today'
        return context
