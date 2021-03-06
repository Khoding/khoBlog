from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import EditPostCommentForm, PostForm, CommentForm, EditForm, CategoryAddForm, CategoryEditForm, ARPostCommentForm
from .models import Post, Comment, Category


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


class PostListFromCategoryView(ListView):
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
        context['title'] = self.category.name
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
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        self.post = get_object_or_404(
            Post, slug=self.kwargs['slug'])
        self.post.clicked()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.filter(
            published_date__lte=timezone.now(), withdrawn=False).order_by('-published_date')
        context['title'] = 'Post Detail'
        context['now'] = timezone.now()
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
class PostFutureListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 21

    def get_queryset(self):
        return self.model.objects.filter(published_date__gte=timezone.now(), withdrawn=False).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Future'
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
        context['now'] = timezone.now()
        context['title'] = 'Withdrawn'
        return context


@superuser_required()
class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_new.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Post'
        return context


@superuser_required()
class AddCategoryView(CreateView):
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
class EditCategoryView(UpdateView):
    model = Category
    form_class = CategoryEditForm
    template_name = "blog/category_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Category'
        return context


@superuser_required()
class EditPostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = "blog/post_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        return context


@superuser_required()
class DeletePostView(DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy('blog:post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Post'
        return context


class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if self.request.user.is_superuser:
            return self.model.objects.filter(
                Q(title__icontains=query) | Q(
                    body__icontains=query) | Q(description__icontains=query),
            )
        else:
            return self.model.objects.filter(
                Q(title__icontains=query) | Q(
                    body__icontains=query) | Q(description__icontains=query),
            ).filter(~Q(published_date__gt=timezone.now()), ~Q(published_date__isnull=True), ~Q(withdrawn=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search in Posts'
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


class AddPostCommentView(LoginRequiredMixin, CreateView):
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


class AddReplyToComment(LoginRequiredMixin, CreateView):
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


class EditPostCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = EditPostCommentForm
    template_name = 'blog/add_comment_to_post.html'

    def form_valid(self, form):
        form.instance.author_logged = self.request.user
        form.instance.related_post_id = self.kwargs['pk_post']
        form.instance.comment_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Comment'
        return context


@superuser_required()
class ApprovePostCommentView(UpdateView):
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


class RemovePostCommentView(LoginRequiredMixin, UpdateView):
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
