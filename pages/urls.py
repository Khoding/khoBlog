from django.urls import path
from .views import PageDetailView, PageListView, kheee_special_case


app_name = 'pages'
urlpatterns = [
    path('', PageListView.as_view(), name='page_list'),
    path('<slug:slug>/', PageDetailView.as_view(), name='page_detail'),

    path('kheee/', kheee_special_case, name='kheee')
]
