from django.urls import path
from . import views

app_name = "todo"
urlpatterns = [
    path('', views.index, name="list"),
    path('update_task/<int:pk>/', views.updateTask, name="update_task"),
    path('delete/<int:pk>/', views.deleteTask, name="delete"),
]
