from django.urls import path
from .views import PageDetailView, PageListView


app_name = 'pages'
urlpatterns = [
    path('', PageListView.as_view(), name='page_list'),
    path('<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
]
