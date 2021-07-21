from comments.forms import CustomCommentForm
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic.edit import CreateView
from blog.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomComment
from django.views.generic import UpdateView


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
    form_class = CustomCommentForm

    def get_queryset(self):
        self.comment = get_object_or_404(CustomComment, pk=self.kwargs['pk'])
        return super().get_queryset()

    def form_valid(self, form):
        form.instance.related_post_id = self.kwargs['pk_post']
        form.instance.parent = self.comment
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(
            published_date__lte=timezone.now(), withdrawn=False, is_removed=False)
        context['title'] = 'Reply to Comment'
        context['side_title'] = 'Post List'
        return context
