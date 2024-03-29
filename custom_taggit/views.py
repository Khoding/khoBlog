from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from khoBlog.utils.superuser_required import superuser_required_ignore_secure_mode

from .filters import TagFilter
from .forms import TagForm
from .models import CustomTag


class TagListView(ListView):
    """TagListView ListView

    List of Tags

    Args:
        ListView ([type]): [description]

    Returns:
        tags: A list of tags
    """

    model = CustomTag
    template_name = "blog/lists/tag_list.html"
    context_object_name = "tags"
    paginate_by = 20
    paginate_orphans = 5

    def get_queryset(self):
        """Get queryset"""
        query = TagFilter(
            self.request.GET,
            queryset=CustomTag.objects.filter(withdrawn=False),
        )
        if self.request.user.is_superuser and self.request.user.secure_mode is False:
            query = TagFilter(
                self.request.GET,
                queryset=CustomTag.objects.all(),
            )
        if query is not None and query != "":
            return query.qs
        if self.request.user.is_superuser and self.request.user.secure_mode is False:
            return self.model.objects.filter(deleted_at=None)
        return self.model.objects.filter(withdrawn=False, deleted_at=None)

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Tag List"
        context["description"] = "List of all tags"
        context["filter_form"] = TagFilter()
        return context


@superuser_required_ignore_secure_mode()
class TagUpdateView(UpdateView):
    """TagUpdateView UpdateView

    A view to Update a Tag

    Args:
        UpdateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = CustomTag
    form = TagForm
    fields = "__all__"
    template_name = "blog/edit_tag.html"
    success_url = reverse_lazy("custom_taggit:tag_list")

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Tag"
        return context
