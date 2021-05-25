from django.urls import path
from django.urls.conf import include

from . import views

task_action_extra_patterns = [
    path('update/', views.TaskUpdateView.as_view(), name="update_task"),
    path('delete/', views.TaskDeleteView.as_view(), name="delete"),
]

app_name = "todo"
urlpatterns = [
    path('', views.TaskListView.as_view(), name="task_list"),
    path('add/', views.TaskCreateView.as_view(), name="create_task"),
    path('<int:pk>/', include(task_action_extra_patterns)),
]
