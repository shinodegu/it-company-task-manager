from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Position, TaskType, Worker, Task


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