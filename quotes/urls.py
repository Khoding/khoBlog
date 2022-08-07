from django.urls import path

from quotes.views import PersonDetailView, QuoteDetailView, SourceDetailView

app_name = "quotes"
urlpatterns = [
    path("<slug:slug>/", QuoteDetailView.as_view(), name="quote_detail"),
    path("person/<slug:slug>/", PersonDetailView.as_view(), name="person_detail"),
    path("source/<slug:slug>/", SourceDetailView.as_view(), name="source_detail"),
]
