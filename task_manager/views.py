from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Position, TaskType, Worker, Task


class IndexView(generic.TemplateView):
    template_name = "task_manager/index.html"