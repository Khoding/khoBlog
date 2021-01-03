from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView

from .models import FlatPage


class PageDetailView(DetailView):
    model = FlatPage
    template_name = 'pages/page.html'

    def get_queryset(self):
        self.page = get_object_or_404(
            FlatPage, slug=self.kwargs['slug'])
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = self.model.objects.all().order_by('-pk')
        context['title'] = self.page.title
        context['now'] = timezone.now()
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
        return context
