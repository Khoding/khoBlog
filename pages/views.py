from django.shortcuts import get_object_or_404, redirect
from django.urls.base import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from pages.forms import FlatPageAddForm, FlatPageEditForm

from .models import FlatPage


class PageDetailView(DetailView):
    model = FlatPage
    template_name = 'flatpages/default.html'

    def get_queryset(self):
        self.page = get_object_or_404(
            FlatPage, slug=self.kwargs['slug'])
        if self.request.user.is_superuser:
            self.title = self.page.title
            self.description = self.page.description
            self.pages = self.model.objects.all().order_by('-pk')
        else:
            if self.page.withdrawn:
                self.title = 'Withdrawn'
                self.description = 'This page is Withdrawn'
                self.pages = self.model.objects.filter(
                    withdrawn=False).order_by('-pk')
            else:
                self.title = self.page.title
                self.description = self.page.description
                self.pages = self.model.objects.filter(
                    withdrawn=False).order_by('-pk')
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = self.pages
        context['title'] = self.title
        context['description'] = self.description
        context['side_title'] = 'Page List'
        context['comment_next'] = self.page.get_absolute_url()
        return context


class PageListView(ListView):
    model = FlatPage
    template_name = 'pages/page_list.html'
    context_object_name = 'pages'
    paginate_by = 21
    paginate_orphans = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(
                withdrawn=False)

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
