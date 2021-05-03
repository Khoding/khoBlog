"""
Vues utilisées uniquement en développement.
"""

from django.views.generic import TemplateView


class Error400View(TemplateView):
    """
    Vue de test de la page d'erreur 400.
    """

    template_name = '400.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Error 400'
        return context


class Error403View(TemplateView):
    """
    Vue de test de la page d'erreur 403.
    """

    template_name = '403.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Error 403'
        return context


class Error404View(TemplateView):
    """
    Vue de test de la page d'erreur 404.
    """

    template_name = '404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Error 404'
        return context


class Error500View(TemplateView):
    """
    Vue de test de la page d'erreur 500.
    """

    template_name = '500.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Error 500'
        return context
