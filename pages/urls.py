from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.index, {'pagename': ''}, name='home'),
    path('<str:pagename>', views.index, name='index'),
]
