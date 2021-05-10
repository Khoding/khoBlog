from django.urls.base import reverse_lazy
from pages.forms import FlatPageAddForm, FlatPageEditForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import FlatPage


class PageDetailView(DetailView):
    model = FlatPage
    template_name = 'flatpages/default.html'

    def get_queryset(self):
        self.page = get_object_or_404(
            FlatPage, slug=self.kwargs['slug'])
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = self.model.objects.all().order_by('-pk')
        context['title'] = self.page.title
        context['description'] = self.page.description
        context['side_title'] = 'Page List'
        context['comment_next'] = self.page.get_absolute_url()
        return context


class PageListView(ListView):
    model = FlatPage
    template_name = 'pages/page_list.html'
    context_object_name = 'pages'

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Page List'
        context['description'] = "List of all Pages"
        return context


class PageCreateView(CreateView):
    model = FlatPage
    template_name = 'pages/page_add.html'
    form_class = FlatPageAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Page'
        context['description'] = "Create a Page"
        return context


class PageUpdateView(UpdateView):
    model = FlatPage
    template_name = 'pages/page_update.html'
    form_class = FlatPageEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Page'
        context['description'] = "Update a Page"
        return context


class PageDeleteView(DeleteView):
    model = FlatPage
    template_name = "pages/page_confirm_delete.html"
    success_url = reverse_lazy('pages:page_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Page'
        return context


def kheee_special_case(request, slug, *args):
    url = get_object_or_404(FlatPage, slug='kheee')
    return redirect(url)
