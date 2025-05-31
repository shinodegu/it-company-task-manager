from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin)
from .models import Position, TaskType, Worker, Task, Tag


class IndexView(generic.TemplateView):
    template_name = "task_manager/index.html"


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type"
    ).prefetch_related(
        "assignees",  # ✅ ManyToMany → prefetch
        "tags"
    )
    paginate_by = 10


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type"
    ).prefetch_related(
        "assignees",
        "tags"
    )


class TaskCreateView(generic.CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    fields =  "is_completed"
    success_url = reverse_lazy("task_manager:task-list")


class WorkerListView(generic.ListView):
    model = Worker
    queryset = Worker.objects.select_related("position")
    paginate_by = 10


class WorkerDetailView(generic.DetailView):
    model = Worker
    queryset = Worker.objects.select_related("position")


class WorkerDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")

    def test_func(self):
        return self.request.user.is_superuser


class WorkerUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Worker
    fields = "__all__"
    success_url = reverse_lazy("task_manager:worker-list")

    def test_func(self):
        return self.request.user.is_superuser


class WorkerCreateView(UserPassesTestMixin, generic.CreateView):
    model = Worker
    fields = "__all__"

    def test_func(self):
        return self.request.user.is_superuser


class TaskTypeListView(generic.ListView):
    model = TaskType
    paginate_by = 10


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeUpdateView(generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task-type-list")


class PositionCreateView(UserPassesTestMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:worker-list")

    def test_func(self):
        return self.request.user.is_superuser


class PositionUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:worker-list")

    def test_func(self):
        return self.request.user.is_superuser


class PositionDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:worker-list")

    def test_func(self):
        return self.request.user.is_superuser


class TagListView(generic.ListView):
    model = Tag
    paginate_by = 10


class TagCreateView(generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tag-list")


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tag-list")


class TagDeleteView(generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")
