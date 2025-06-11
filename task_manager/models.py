from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="workers")

    def __str__(self):
        return f"{self.username}: {self.position.name}"

    def get_absolute_url(self):
        return reverse("worker-detail", kwargs={"pk": self.pk})


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "Urgent"
        HIGH = "High"
        MEDIUM = "Medium"
        LOW = "Low"
    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(Worker, related_name="assigned_tasks")
    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True)

    def __str__(self):
        return f"{self.name}: {self.task_type.name}, {self.priority}, {self.deadline}"

    def get_absolute_url(self):
        return reverse("task-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["is_completed", "deadline"]


