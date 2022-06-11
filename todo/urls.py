from django.urls import path
from django.urls.conf import include

from .views import TaskChangeStatusView, TaskCreateView, TaskDeleteView, TaskListView, TaskUpdateView

task_action_extra_patterns = [
    path("change_status/", TaskChangeStatusView.as_view(), name="task_change_status"),
    path("edit/", TaskUpdateView.as_view(), name="edit_task"),
    path("delete/", TaskDeleteView.as_view(), name="delete"),
]

app_name = "todo"
urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("add/", TaskCreateView.as_view(), name="create_task"),
    path("<int:pk>/", include(task_action_extra_patterns)),
]
