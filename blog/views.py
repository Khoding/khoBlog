from blog.filters import PostFilter
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.dates import (ArchiveIndexView, DateDetailView,
                                        DayArchiveView, MonthArchiveView,
                                        TodayArchiveView, WeekArchiveView,
                                        YearArchiveView)
from rules.contrib.views import AutoPermissionRequiredMixin
from custom_taggit.models import CustomTag
from django.core.exceptions import PermissionDenied

from .forms import (ARPostCommentForm, CategoryAddForm, CategoryDeleteForm, CategoryEditForm,
                    CommentForm, EditPostCommentForm, PostAddForm, PostDeleteForm,
                    PostEditForm, SeriesAddForm, SeriesDeleteForm, SeriesEditForm)
from .models import Category, Comment, Post, PostContent, Series


def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass

    return wrapper


class PostListView(ListView):
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


class PostInCategoryListView(ListView):
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
    model = Post
    template_name = 'blog/lists/post_series_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        self.series = get_object_or_404(
            Series, slug=self.kwargs['slug'])
        return self.model.objects.get_common_queryset(self.request.user).filter(series=self.series).order_by('order_in_series')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['series'] = self.series
        context['title'] = self.series.title
        context['side_title'] = 'Post List'
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/lists/category_list.html'
    context_object_name = 'category_list'
    paginate_by = 21
    paginate_orphans = 5
    ordering = 'pk'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.get_without_removed()
        else:
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
    model = Series
    template_name = 'blog/lists/series_list.html'
    context_object_name = 'series_list'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.get_without_removed()
        else:
            return self.model.objects.filter(withdrawn=False).get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Series List'
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        self.post = get_object_or_404(Post, slug=self.kwargs['slug'])
        self.post.clicked()
        if self.post.is_removed:
            raise PermissionDenied
        elif self.request.user.is_superuser:
            self.series = self.model.objects.get_common_queryset(self.request.user).filter(
                series__isnull=False, series=self.post.series).order_by('order_in_series')
            self.title = self.post.title
            self.description = self.post.description
        else:
            self.series = self.model.objects.get_common_queryset(self.request.user).filter(
                series__isnull=False, series=self.post.series).order_by('order_in_series')
            if self.post.withdrawn or not self.post.published_date or self.post.published_date >= timezone.now():
                raise PermissionDenied
            else:
                self.title = self.post.title
                self.description = self.post.description
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
        return context


def redirect_to_latest(request):
    latest = Post.objects.latest('id')
    return redirect(reverse('blog:post_detail', args=(latest.slug,)))


def post_detail_through_id(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return redirect(reverse('blog:post_detail', args=(post.slug,)))


@superuser_required()
class PostDraftListView(ListView):
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
    model = CustomTag
    template_name = 'blog/lists/tags_list.html'
    context_object_name = 'tags'
    paginate_by = 21
    paginate_orphans = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tag List"
        context['description'] = "List of all tags"
        context['side_title'] = 'Tag List'
        context['search_url'] = reverse('blog:tag_search_results')
        context['search_title'] = "Search in Tags"
        return context


class PostWithTagListView(ListView):
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
    model = Post
    form_class = PostAddForm
    template_name = "blog/post_new.html"

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
    model = Category
    form_class = CategoryAddForm
    template_name = "blog/category_new.html"

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
    model = Series
    form_class = SeriesAddForm
    template_name = "blog/series_new.html"

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.get_without_removed().order_by(
            '-pk')
        context['title'] = 'New Series'
        context['side_title'] = 'Series List'
        return context


class CategoryUpdateView(AutoPermissionRequiredMixin, UpdateView):
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


class PostDeleteView(AutoPermissionRequiredMixin, UpdateView):
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
    template_name = 'blog/search.html'
    context_object_name = 'query'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        query = [[{'id': 1, 'title': 'Search in Posts', 'get_absolute_url': 'post/?q=', }, {'id': 2, 'title': 'Search in Categories', 'get_absolute_url': 'category/?q=', },
                  {'id': 3, 'title': 'Search in Tags', 'get_absolute_url': 'tag/?q=', }, {'id': 4, 'title': 'Search in Everything', 'get_absolute_url': 'all/?q='}, ]]
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search'
        context['search_url'] = reverse('blog:search_results')
        context['search_title'] = "Search in Everything"
        return context


class PostSearchResultsListView(ListView):
    model = Post
    template_name = 'blog/search.html'
    context_object_name = 'filter'
    # paginate_by = 21
    # paginate_orphans = 5

    def get_queryset(self):
        self.f = PostFilter(self.request.GET,
                            queryset=self.model.objects.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search in Posts'
        context['search_url'] = reverse('blog:post_search_results')
        context['search_title'] = "Search in Posts"
        context['filter'] = self.f
        return context


class CategorySearchResultsListView(ListView):
    model = Category
    template_name = 'blog/search.html'
    context_object_name = 'query'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query != None:
            if self.request.user.is_superuser:
                return self.model.objects.filter(
                    Q(title__icontains=query) | Q(
                        description__icontains=query),
                ).get_without_removed()
            else:
                return self.model.objects.filter(
                    Q(title__icontains=query) | Q(
                        description__icontains=query),
                ).filter(~Q(withdrawn=True),
                         ).get_without_removed()
        else:
            if self.request.user.is_superuser:
                category = self.model.objects.get_without_removed()
                return category
            else:
                category = self.model.objects.filter(
                    ~Q(withdrawn=True),).get_without_removed()
                return category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search in Categories'
        context['search_url'] = reverse('blog:category_search_results')
        context['search_title'] = "Search in Categories"
        return context


class TagsSearchResultsListView(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'query'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query != None:
            return CustomTag.objects.filter(
                Q(name__icontains=query)
            )
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
    template_name = 'blog/search.html'
    context_object_name = 'query'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query != None:
            if self.request.user.is_superuser:
                post = Post.objects.filter(
                    Q(title__icontains=query) | Q(
                        body__icontains=query) | Q(description__icontains=query),
                ).get_without_removed()
                category = Category.objects.filter(
                    Q(title__icontains=query) | Q(
                        description__icontains=query),
                ).get_without_removed()
                tag = CustomTag.objects.filter(
                    Q(name__icontains=query)
                )
                return [post, category, tag]
            else:
                post = Post.objects.filter(
                    Q(title__icontains=query) | Q(
                        body__icontains=query) | Q(description__icontains=query),
                ).filter(~Q(published_date__gt=timezone.now()), ~Q(published_date__isnull=True), ~Q(withdrawn=True),
                         ).get_without_removed()
                category = Category.objects.filter(
                    Q(title__icontains=query) | Q(
                        description__icontains=query),
                ).filter(~Q(withdrawn=True),
                         ).get_without_removed()
                tag = CustomTag.objects.filter(
                    Q(name__icontains=query)
                )
                return [post, category, tag]
        else:
            if self.request.user.is_superuser:
                post = Post.objects.get_without_removed()
                category = Category.objects.get_without_removed()
                tag = CustomTag.objects.all()
                return [post, category, tag]
            else:
                post = Post.objects.filter(~Q(published_date__gt=timezone.now()), ~Q(
                    published_date__isnull=True), ~Q(withdrawn=True),).get_without_removed()
                category = Category.objects.filter(
                    ~Q(withdrawn=True),).get_without_removed()
                tag = CustomTag.objects.all()
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
        return self.model.objects.get_common_queryset(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Post archives'
        return context


class PostYearArchiveView(YearArchiveView):
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
        return self.model.objects.get_base_common_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted during ' + str(self.get_year())
        return context


class PostMonthArchiveView(MonthArchiveView):
    model = Post
    template_name = 'blog/lists/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5
    allow_empty = True
    date_field = "published_date"
    allow_future = True

    def get_queryset(self):
        return self.model.objects.get_base_common_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted during ' + \
            str(self.get_month()) + \
            ' of ' + str(self.get_year())
        return context


class PostWeekArchiveView(WeekArchiveView):
    model = Post
    template_name = 'blog/lists/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5
    date_field = 'published_date'
    week_format = '%W'
    allow_future = True

    def get_queryset(self):
        return self.model.objects.get_base_common_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted during Week ' + \
            str(self.get_week()) + ' of ' + str(self.get_year())
        return context


class PostDayArchiveView(DayArchiveView):
    model = Post
    template_name = 'blog/lists/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5
    date_field = 'published_date'
    allow_future = True

    def get_queryset(self):
        return self.model.objects.get_base_common_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted the ' + \
            str(self.get_day()) + ' ' + str(self.get_month()) + \
            ' ' + str(self.get_year())
        return context


class PostDateDetailView(DateDetailView):
    model = Post
    template_name = 'blog/archive_date_detail.html'
    date_field = "published_date"

    def get_queryset(self):
        self.post = get_object_or_404(Post, slug=self.kwargs['slug'])
        self.post.clicked()
        if self.post.is_removed:
            raise PermissionDenied
        elif self.request.user.is_superuser:
            self.series = self.model.objects.get_common_queryset(self.request.user).filter(
                series__isnull=False, series=self.post.series).order_by('order_in_series')
            self.title = self.post.title
            self.description = self.post.description
        else:
            self.series = self.model.objects.get_common_queryset(self.request.user).filter(
                series__isnull=False, series=self.post.series).order_by('order_in_series')
            if self.post.withdrawn or not self.post.published_date or self.post.published_date >= timezone.now():
                raise PermissionDenied
            else:
                self.title = self.post.title
                self.description = self.post.description
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
        return context


class PostTodayArchiveView(TodayArchiveView):
    model = Post
    template_name = 'blog/lists/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    paginate_orphans = 5
    allow_empty = True
    date_field = "published_date"
    allow_future = True

    def get_queryset(self):
        return self.model.objects.get_base_common_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted today'
        return context
