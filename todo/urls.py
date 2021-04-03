from django.urls import path
from . import views

app_name = "todo"
urlpatterns = [
    path('', views.TaskListView.as_view(), name="list"),
    path('create/', views.TaskCreateView.as_view(), name="create_task"),
    path('update_task/<int:pk>/', views.TaskUpdateView.as_view(), name="update_task"),
    path('delete/<int:pk>/', views.TaskDeleteView.as_view(), name="delete"),
]
