from django.urls import path
from .views import (
    IndexView,
    TaskListView, TaskDetailView,
    TaskCreateView, TaskUpdateView,
    WorkerListView, WorkerDetailView,
    WorkerCreateView, WorkerDeleteView,
    PositionCreateView, WorkerPositionUpdateView,
    PositionUpdateView, PositionDeleteMultiView,
    TaskTypeListView, TaskTypeCreateView,
    TaskTypeUpdateView, TaskTypeDeleteView,
    TagListView, TagCreateView,
    TagUpdateView, TagDeleteView
)

app_name = "task_manager"

urlpatterns = [
    # Home
    path("", IndexView.as_view(), name="index"),

    # Tasks
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),

    # Workers
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/update/", WorkerPositionUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),

    # Positions
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    path("positions/delete-multi/", PositionDeleteMultiView.as_view(), name="position-delete-multi"),


    # Task Types
    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task-types/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task-types/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task-types/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="task-type-delete"),

    # Tags
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/create/", TagCreateView.as_view(), name="tag-create"),
    path("tags/<int:pk>/update/", TagUpdateView.as_view(), name="tag-update"),
    path("tags/<int:pk>/delete/", TagDeleteView.as_view(), name="tag-delete"),
]
