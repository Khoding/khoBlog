from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from .models import Page


class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/page.html'

    def get_queryset(self):
        self.page = get_object_or_404(
            Page, slug=self.kwargs['slug'])
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = self.model.objects.all().order_by('-pk')
        context['title'] = self.page.title
        context['now'] = timezone.now()
        return context


class PageIndexView(TemplateView):
    model = Page
    template_name = 'pages/page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = self.model.objects.all().order_by('-pk')
        context['title'] = 'Pages'
        context['content'] = 'Pages, hf <a href="khodok">Khodok</a>'
        context['now'] = timezone.now()
        return context
