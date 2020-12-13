from django.urls import path
from .views import PageDetailView, PageIndexView


app_name = 'pages'
urlpatterns = [
    path('', PageIndexView.as_view(), name='page_index'),
    path('<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
]
