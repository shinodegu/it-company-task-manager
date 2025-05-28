from django.urls import path
from .views import (IndexView,
                    TaskListView, TaskDetailView)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]

app_name = "task_manager"