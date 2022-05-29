from django.views.generic import DetailView

from quotes.models import Quote


class QuoteDetailView(DetailView):
    model = Quote
    template_name = "quotes/quote_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quote"] = self.object
        context["title"] = self.object.author
        context["description"] = self.object.body
        return context
