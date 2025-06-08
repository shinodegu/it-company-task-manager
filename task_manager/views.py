from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin)

from .forms import (TaskForm, WorkerPositionUpdateForm,
                    WorkerForm, PositionDeleteForm, WorkerSearchForm, TaskSearchForm)
from .models import Position, TaskType, Worker, Task, Tag


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "task_manager/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            tasks = Task.objects.filter(
                assignees=self.request.user
            ).select_related("task_type")[:3]
            if not tasks.exists():
                tasks = Task.objects.all().select_related("task_type")[:3]
        else:
            tasks = Task.objects.all().select_related("task_type")[:3]

        context["tasks"] = tasks
        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type"
    ).prefetch_related(
        "assignees",  # ✅ ManyToMany → prefetch
        "tags"
    )
    paginate_by = 9

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type").prefetch_related("assignees", "tags")
        form = TaskSearchForm(self.request.GET)

        if form.is_valid() and form.cleaned_data["title"]:
            title = form.cleaned_data["title"]
            queryset = queryset.filter(name__icontains=title)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskSearchForm(self.request.GET)
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type"
    ).prefetch_related(
        "assignees",
        "tags"
    )


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 10

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        form = WorkerSearchForm(self.request.GET)

        if form.is_valid() and form.cleaned_data["title"]:
            title = form.cleaned_data["title"]
            queryset = queryset.filter(username__icontains=title)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = WorkerSearchForm(self.request.GET)
        return context


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.select_related("position")


class WorkerDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")

    def test_func(self):
        return self.request.user.is_superuser


class WorkerCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy("task_manager:worker-list")

    def test_func(self):
        return self.request.user.is_superuser


class WorkerPositionUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerPositionUpdateForm
    success_url = reverse_lazy("task_manager:worker-list")

    def test_func(self):
        return self.request.user.is_superuser

class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 10


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task-type-list")


class PositionCreateView(LoginRequiredMixin,
                         UserPassesTestMixin,
                         generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:worker-list")

    def test_func(self):
        return self.request.user.is_superuser


class PositionUpdateView(LoginRequiredMixin,
                         UserPassesTestMixin,
                         generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:worker-list")

    def test_func(self):
        return self.request.user.is_superuser


class PositionDeleteMultiView(LoginRequiredMixin, UserPassesTestMixin, generic.FormView):
    template_name = "task_manager/position_delete_multi.html"
    form_class = PositionDeleteForm
    success_url = reverse_lazy("task_manager:worker-list")

    def form_valid(self, form):
        positions = form.cleaned_data["positions"]
        positions.delete()
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 10


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tag-list")


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tag-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")
