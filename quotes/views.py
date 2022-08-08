from django.views.generic import DetailView

from quotes.models import Person, Quote, Source


class QuoteDetailView(DetailView):
    """QuoteDetailView Class"""

    model = Quote
    template_name = "quotes/quote_detail.html"

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["quote"] = self.object
        context["title"] = self.object.author
        context["description"] = self.object.body
        return context


class PersonDetailView(DetailView):
    """PersonDetailView Class"""

    model = Person
    template_name = "quotes/specific_detail.html"

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = self.object
        context["description"] = f"Quotes involving {self.object}"
        return context


class SourceDetailView(DetailView):
    """SourceDetailView Class"""

    model = Source
    template_name = "quotes/specific_detail.html"

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = self.object
        context["description"] = f"Quotes in {self.object}"
        return context
