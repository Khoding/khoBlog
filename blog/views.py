from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic.dates import ArchiveIndexView, DateDetailView, DayArchiveView, MonthArchiveView, WeekArchiveView, YearArchiveView, TodayArchiveView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import EditPostCommentForm, PostAddForm, CommentForm, PostEditForm, CategoryAddForm, CategoryEditForm, ARPostCommentForm, SeriesAddForm, SeriesEditForm
from .models import Post, Comment, Category, Series


def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass

    return wrapper


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21

    def get_queryset(self):
        return self.model.objects.filter(published_date__lte=timezone.now(), withdrawn=False).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Latest Posts'
        context['featured'] = self.model.objects.filter(
            featured=True, big=False)
        context['featured_big'] = self.model.objects.filter(
            featured=True, big=True)
        context['featured_cat'] = self.model.objects.filter(
            post_to_category__featured_cat=True)
        return context


class PostInCategoryListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, slug=self.kwargs['slug'])
        if self.request.user.is_superuser:
            return self.model.objects.filter(categories=self.category).order_by('-published_date')
        else:
            return self.model.objects.filter(published_date__lte=timezone.now(), withdrawn=False, categories=self.category).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = self.category
        context['title'] = self.category.title
        return context


class PostInSeriesListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21

    def get_queryset(self):
        self.series = get_object_or_404(
            Series, slug=self.kwargs['slug'])
        if self.request.user.is_superuser:
            return self.model.objects.filter(series=self.series).order_by('post_order_in_series')
        else:
            return self.model.objects.filter(published_date__lte=timezone.now(), withdrawn=False, series=self.series).order_by('post_order_in_series')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['series'] = self.series
        context['title'] = self.series.title
        return context


class CategoryListView(ListView):
    model = Category
    template = 'blog/category_list.html'
    context_object_name = 'category_list'
    paginate_by = 21
    ordering = 'pk'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(withdrawn=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Category List'
        context['search_url'] = reverse('blog:category_search_results')
        return context


class SeriesListView(ListView):
    model = Series
    template = 'blog/series_list.html'
    context_object_name = 'series_list'
    paginate_by = 21

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(withdrawn=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Series List'
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        self.post = get_object_or_404(
            Post, slug=self.kwargs['slug'])
        self.post.clicked()
        if self.request.user.is_superuser:
            self.series = self.model.objects.filter(
                series__isnull=False, series=self.post.series).order_by('post_order_in_series')
        else:
            self.series = self.model.objects.filter(
                series__isnull=False, series=self.post.series, published_date__lte=timezone.now(), withdrawn=False).order_by('post_order_in_series')
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.filter(
            published_date__lte=timezone.now(), withdrawn=False).order_by('post_order_in_series')
        context['title'] = 'Post Detail'
        context['series'] = self.series
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
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21

    def get_queryset(self):
        return self.model.objects.filter(published_date__isnull=True).order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Drafts'
        return context


@superuser_required()
class PostScheduledListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21

    def get_queryset(self):
        return self.model.objects.filter(published_date__gte=timezone.now(), withdrawn=False).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Scheduled'
        return context


@superuser_required()
class PostWithdrawnListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21

    def get_queryset(self):
        return self.model.objects.filter(withdrawn=True).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Withdrawn'
        return context


@superuser_required()
class PostCreateView(CreateView):
    model = Post
    form_class = PostAddForm
    template_name = "blog/post_new.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Post'
        return context


@superuser_required()
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryAddForm
    template_name = "blog/category_new.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Category'
        return context


@superuser_required()
class SeriesCreateView(CreateView):
    model = Series
    form_class = SeriesAddForm
    template_name = "blog/series_new.html"

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Series'
        return context


@superuser_required()
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryEditForm
    template_name = "blog/category_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Category'
        return context


@superuser_required()
class SeriesUpdateView(UpdateView):
    model = Series
    form_class = SeriesEditForm
    template_name = "blog/series_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Series'
        return context


@superuser_required()
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = "blog/post_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        return context


@superuser_required()
class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy('blog:post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Post'
        return context


class SearchListView(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'query'
    paginate_by = 21

    def get_queryset(self):
        query = [[{'id': 1, 'title': 'Search in Posts', 'get_absolute_url': 'post/?q=', }, {'id': 2, 'title': 'Search in Categories', 'get_absolute_url': 'category/?q=', }, {
            'id': 3, 'title': 'Search in Comments', 'get_absolute_url': 'comment/?q=', }, {'id': 4, 'title': 'Search in Everything', 'get_absolute_url': 'all/?q='}, ]]
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search'
        context['search_url'] = reverse('blog:search_results')
        return context


class PostSearchResultsListView(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'query'
    paginate_by = 21

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query != None:
            if self.request.user.is_superuser:
                return Post.objects.filter(
                    Q(title__icontains=query) | Q(
                        body__icontains=query) | Q(description__icontains=query),
                )
            else:
                return Post.objects.filter(
                    Q(title__icontains=query) | Q(
                        body__icontains=query) | Q(description__icontains=query),
                ).filter(~Q(published_date__gt=timezone.now()), ~Q(published_date__isnull=True), ~Q(withdrawn=True),
                         )
        else:
            if self.request.user.is_superuser:
                post = Post.objects.all()
                return post
            else:
                post = Post.objects.filter(~Q(published_date__gt=timezone.now()), ~Q(
                    published_date__isnull=True), ~Q(withdrawn=True),)
                return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search in Posts'
        context['search_url'] = reverse('blog:post_search_results')
        return context


class CategorySearchResultsListView(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'query'
    paginate_by = 21

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query != None:
            if self.request.user.is_superuser:
                return Category.objects.filter(
                    Q(title__icontains=query) | Q(
                        description__icontains=query),
                )
            else:
                return Category.objects.filter(
                    Q(title__icontains=query) | Q(
                        description__icontains=query),
                ).filter(~Q(withdrawn=True),
                         )
        else:
            if self.request.user.is_superuser:
                category = Category.objects.all()
                return category
            else:
                category = Category.objects.filter(~Q(withdrawn=True),)
                return category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search in Categories'
        context['search_url'] = reverse('blog:category_search_results')
        return context


class CommentSearchResultsListView(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'query'
    paginate_by = 21

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query != None:
            if self.request.user.is_superuser:
                return Comment.objects.filter(
                    Q(title__icontains=query) | Q(author__icontains=query) | Q(
                        body__icontains=query),
                )
            else:
                return Comment.objects.filter(
                    Q(title__icontains=query) | Q(author__icontains=query) | Q(
                        body__icontains=query),
                ).filter(~Q(approbation_state='RE'),
                         )
        else:
            if self.request.user.is_superuser:
                comment = Comment.objects.all()
                return comment
            else:
                comment = Comment.objects.filter(~Q(approbation_state='RE'),)
                return comment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search in Comments'
        context['search_url'] = reverse('blog:comment_search_results')
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
        return context


class AllSearchResultsListView(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'query'
    paginate_by = 21

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query != None:
            if self.request.user.is_superuser:
                post = Post.objects.filter(
                    Q(title__icontains=query) | Q(
                        body__icontains=query) | Q(description__icontains=query),
                )
                category = Category.objects.filter(
                    Q(title__icontains=query) | Q(
                        description__icontains=query),
                )
                comment = Comment.objects.filter(
                    Q(title__icontains=query) | Q(author__icontains=query) | Q(
                        body__icontains=query),
                )
                return [post, category, comment]
            else:
                post = Post.objects.filter(
                    Q(title__icontains=query) | Q(
                        body__icontains=query) | Q(description__icontains=query),
                ).filter(~Q(published_date__gt=timezone.now()), ~Q(published_date__isnull=True), ~Q(withdrawn=True),
                         )
                category = Category.objects.filter(
                    Q(title__icontains=query) | Q(
                        description__icontains=query),
                ).filter(~Q(withdrawn=True),
                         )
                comment = Comment.objects.filter(
                    Q(title__icontains=query) | Q(author__icontains=query) | Q(
                        body__icontains=query),
                ).filter(~Q(approbation_state='RE'),
                         )
                return [post, category, comment]
        else:
            if self.request.user.is_superuser:
                post = Post.objects.all()
                category = Category.objects.all()
                comment = Comment.objects.all()
                return [post, category, comment]
            else:
                post = Post.objects.filter(~Q(published_date__gt=timezone.now()), ~Q(
                    published_date__isnull=True), ~Q(withdrawn=True),)
                category = Category.objects.filter(~Q(withdrawn=True),)
                comment = Comment.objects.filter(~Q(approbation_state='RE'),)
                return [post, category, comment]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search in Everything'
        context['search_url'] = reverse('blog:search_results')
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


class PostCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/add_comment_to_post.html"

    def form_valid(self, form):
        form.instance.author_logged = self.request.user
        form.instance.related_post_id = self.kwargs['pk_post']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Comment'
        return context


class ReplyToCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/add_comment_to_post.html"

    def form_valid(self, form):
        form.instance.author_logged = self.request.user
        form.instance.related_post_id = self.kwargs['pk_post']
        form.instance.comment_answer_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reply to Comment'
        return context


class PostCommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = EditPostCommentForm
    template_name = 'blog/add_comment_to_post.html'

    def form_valid(self, form):
        form.instance.related_post_id = self.kwargs['pk_post']
        form.instance.comment_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Comment'
        return context


@superuser_required()
class ApprovePostCommentUpdateView(UpdateView):
    model = Comment
    form_class = ARPostCommentForm
    template_name = 'blog/ar_post_comment.html'
    success_url = reverse_lazy('blog:post_list')

    def get_queryset(self):
        self.comment = get_object_or_404(
            Comment, pk=self.kwargs['pk'])
        self.comment.approve()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Approve Comment'
        return context


class RemovePostCommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = ARPostCommentForm
    template_name = 'blog/ar_post_comment.html'
    success_url = reverse_lazy('blog:post_list')

    def get_queryset(self):
        self.comment = get_object_or_404(
            Comment, pk=self.kwargs['pk'])
        self.comment.remove()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Remove Comment'
        return context


class PostArchiveIndexView(ArchiveIndexView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    allow_empty = True
    make_object_list = True
    date_field = "published_date"
    allow_future = True

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all().order_by('published_date')
        else:
            return self.model.objects.filter(published_date__lte=timezone.now(), withdrawn=False).order_by('published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Post archives'
        return context


class PostYearArchiveView(YearArchiveView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    allow_empty = True
    make_object_list = True
    date_field = "published_date"
    allow_future = True

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all().order_by('published_date')
        else:
            return self.model.objects.filter(published_date__lte=timezone.now(), withdrawn=False).order_by('published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted during ' + str(self.get_year())
        return context


class PostMonthArchiveView(MonthArchiveView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    allow_empty = True
    date_field = "published_date"
    allow_future = True

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all().order_by('published_date')
        else:
            return self.model.objects.filter(published_date__lte=timezone.now(), withdrawn=False).order_by('published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted during ' + \
            str(self.get_month()) + \
            ' of ' + str(self.get_year())
        return context


class PostWeekArchiveView(WeekArchiveView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    date_field = "published_date"
    week_format = "%W"
    allow_future = True

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all().order_by('published_date')
        else:
            return self.model.objects.filter(published_date__lte=timezone.now(), withdrawn=False).order_by('published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted during Week ' + \
            str(self.get_week()) + ' of ' + str(self.get_year())
        return context


class PostDayArchiveView(DayArchiveView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    date_field = "published_date"
    allow_future = True

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all().order_by('published_date')
        else:
            return self.model.objects.filter(published_date__lte=timezone.now(), withdrawn=False).order_by('published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted the ' + \
            str(self.get_day()) + ' ' + str(self.get_month()) + \
            ' ' + str(self.get_year())
        return context


class PostTodayArchiveView(TodayArchiveView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21
    allow_empty = True
    date_field = "published_date"
    allow_future = True

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all().order_by('published_date')
        else:
            return self.model.objects.filter(published_date__lte=timezone.now(), withdrawn=False).order_by('published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '[Archive] Posted today'
        return context
