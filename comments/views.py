from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class CommentListView(LoginRequiredMixin, TemplateView):
    """CommentListView

    A list of all comments
    """

    template_name = "blog/comments/comment_list.html"

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Comment List"
        context["description"] = "List of all comments"
        return context
