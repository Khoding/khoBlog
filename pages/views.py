from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.urls.base import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, ListView, UpdateView

from pages.forms import PageAddForm, PageDeleteForm, PageEditForm

from .models import Page

DEFAULT_TEMPLATE = "pages/default.html"


def page(request, slug):
    """
    Public interface to the flat page view.

    Models: `pages.pages`
    Templates: Uses the template defined by the ``template_name`` field,
        or :template:`pages/default.html` if template_name is not defined.
    Context:
        page
            `pages.pages` object
    """
    site_id = get_current_site(request).id
    try:
        f = get_object_or_404(Page, slug=slug, sites=site_id)
    except Http404:
        f = get_object_or_404(Page, slug=slug, sites=site_id)
        return HttpResponsePermanentRedirect("%s/" % request.path)
    return render_page(request, f)


@csrf_protect
def render_page(request, f):
    """Internal interface to the flat page view."""
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated:
        from django.contrib.auth.views import redirect_to_login

        return redirect_to_login(request.path)
    if f.deleted_at:
        raise Http404
    if f.template_name:
        template = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    else:
        template = loader.get_template(DEFAULT_TEMPLATE)

    # To avoid having to always use the "|safe" filter in page templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.title = mark_safe(f.title)  # skipcq: BAN-B308
    f.content = mark_safe(f.content)  # skipcq: BAN-B308

    return HttpResponse(template.render({"page": f, "title": f.title, "description": f.description}, request))


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
        """Get queryset"""
        if self.request.user.is_superuser and not self.request.user.secure_mode is True:
            return self.model.objects.filter(deleted_at=None)
        return self.model.objects.filter(withdrawn=False, deleted_at=None)

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Page List"
        context["description"] = "List of all Pages"
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
        """Get context data"""
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
        """Get context data"""
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
        """Get queryset"""
        if self.request.user.is_superuser and not self.request.user.secure_mode is True:
            removing_page = get_object_or_404(Page, slug=self.kwargs["slug"])
            if self.get_form().is_valid():
                removing_page.soft_delete()
        else:
            raise PermissionDenied
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Page"
        context["description"] = "Delete a Page"
        return context


def kheee_page():
    """kheee_page

    A direct link to kheee Page
    """
    url = get_object_or_404(Page, slug="kheee")
    return redirect(url)


def about_page():
    """about_page

    A direct link to about Page
    """
    url = get_object_or_404(Page, slug="about")
    return redirect(url)


def quotes_page():
    """quotes_page

    A direct link to quotes Page
    """
    url = get_object_or_404(Page, slug="quotes")
    return redirect(url)
