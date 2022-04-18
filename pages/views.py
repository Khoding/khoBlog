from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from pages.forms import PageAddForm, PageDeleteForm, PageEditForm

from .models import Page


class PageDetailView(DetailView):
    """PageDetailView

    Details of a Page

    Args:
        DetailView ([type]): [description]

    Raises:
        PermissionDenied: [description]

    Returns:
        [type]: [description]
    """

    model = Page
    template_name = "flatpages/default.html"

    def get_queryset(self):
        self.page = get_object_or_404(Page, slug=self.kwargs["slug"])
        if self.page.is_removed:
            raise PermissionDenied
        if self.request.user.is_superuser:
            self.title = self.page.title
            self.description = self.page.description
            self.pages = self.model.objects.filter(is_removed=False).order_by("-pk")
        else:
            if self.page.withdrawn:
                self.title = "Withdrawn"
                self.description = "This page is Withdrawn"
                self.pages = self.model.objects.filter(withdrawn=False, is_removed=False).order_by("-pk")
            else:
                self.title = self.page.title
                self.description = self.page.description
                self.pages = self.model.objects.filter(withdrawn=False, is_removed=False).order_by("-pk")
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pages"] = self.pages
        context["title"] = self.title
        context["description"] = self.description
        return context


class PageListView(ListView):
    """PageListView

    A list of Pages

    Args:
        ListView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Page
    template_name = "pages/page_list.html"
    context_object_name = "pages"
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.filter(is_removed=False)
        return self.model.objects.filter(withdrawn=False, is_removed=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Page List"
        context["description"] = "List of all Pages"
        context["content_type"] = "page"
        return context


class PageCreateView(CreateView):
    """PageCreateView

    A view for creating a Page

    Args:
        CreateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Page
    template_name = "pages/create_page.html"
    form_class = PageAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Page"
        context["description"] = "Create a Page"
        return context


class PageUpdateView(UpdateView):
    """PageUpdateView

    A view for updating a Page

    Args:
        UpdateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Page
    template_name = "pages/edit_page.html"
    form_class = PageEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Page"
        context["description"] = "Update a Page"
        return context


class PageDeleteView(UpdateView):
    """PageDeleteView

    View to delete a Page

    Raises:
        PermissionDenied: [description]

    Returns:
        [type]: [description]
    """

    model = Page
    template_name = "pages/page_confirm_delete.html"
    form_class = PageDeleteForm
    success_url = reverse_lazy("pages:index")

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.removing_page = get_object_or_404(Page, slug=self.kwargs["slug"])
            if self.get_form().is_valid():
                self.removing_page.remove()
        else:
            raise PermissionDenied()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Page"
        context["description"] = "Delete a Page"
        return context


def kheee_page():
    """kheee_page

    A direct link to kheee Page

    Returns:
        [type]: [description]
    """
    url = get_object_or_404(Page, slug="kheee")
    return redirect(url)


def about_page():
    """about_page

    A direct link to about Page

    Returns:
        [type]: [description]
    """
    url = get_object_or_404(Page, slug="about")
    return redirect(url)
