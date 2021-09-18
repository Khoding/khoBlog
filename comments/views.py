from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView

from blog.models import Post
from .models import CustomComment


class CommentListView(LoginRequiredMixin, ListView):
    model = CustomComment
    template_name = 'blog/comments/comment_list.html'
    context_object_name = 'comment_list'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        return self.model.objects.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Comment List'
        context['side_title'] = 'Comment List'
        return context


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomComment
    template_name = 'blog/comments/edit_comment.html'
    fields = ('title', 'alias_user', 'comment',)

    def get_queryset(self):
        self.comment = get_object_or_404(CustomComment, pk=self.kwargs['pk'])
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(
            published_date__lte=timezone.now(), withdrawn=False, is_removed=False)
        context['title'] = 'Edit Comment'
        context['side_title'] = 'Post List'
        context['comment'] = self.comment
        return context


class CommentReplyView(LoginRequiredMixin, CreateView):
    model = CustomComment
    template_name = 'blog/comments/add_comment_to_post.html'
    fields = ('title', 'alias_user', 'comment',)

    def form_valid(self, form):
        comment = get_object_or_404(CustomComment, pk=self.kwargs['pk'])

        form.instance.content_type_id = comment.content_type.pk
        form.instance.user = self.request.user
        form.instance.object_pk = comment.object_pk
        form.instance.site_id = comment.site.pk
        form.instance.parent_id = comment.pk
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(
            published_date__lte=timezone.now(), withdrawn=False, is_removed=False)
        context['title'] = 'Reply to Comment'
        context['side_title'] = 'Post List'
        return context
