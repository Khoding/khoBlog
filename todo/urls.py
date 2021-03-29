from django.urls import path

from . import views

app_name = 'todo'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.addTodo, name='add'),
    path('<pk>/completion/', views.completion, name='complete'),
    path('<pk>/delete/', views.TodoDeleteView.as_view(), name='delete'),
    path('delete_complete/', views.deleteCompleted, name='delete_complete'),
    path('delete_all/', views.deleteAll, name='delete_all')
]
