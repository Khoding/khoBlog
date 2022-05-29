from django.urls import path

from quotes.views import QuoteDetailView

app_name = "quotes"
urlpatterns = [
    path("<slug:slug>/", QuoteDetailView.as_view(), name="quote_detail"),
]
