from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.models import TaskType, Position, Worker

User = get_user_model()


class AccessControlTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_position = Position.objects.create(name="Admin")
        self.user_position = Position.objects.create(name="User")

        self.admin_user = User.objects.create_superuser(
            username="admin", password="admin123", position=self.admin_position
        )
        self.normal_user = User.objects.create_user(
            username="user", password="user123", position=self.user_position
        )

    def test_admin_can_access_worker_create(self):
        self.client.login(username="admin", password="admin123")
        response = self.client.get(reverse("task_manager:worker-create"))
        self.assertEqual(response.status_code, 200)

    def test_non_admin_cannot_access_worker_create(self):
        self.client.login(username="user", password="user123")
        response = self.client.get(reverse("task_manager:worker-create"))
        self.assertEqual(response.status_code, 403)

    def test_anonymous_redirect_to_login(self):
        response = self.client.get(reverse("task_manager:worker-create"))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('task_manager:worker-create')}"
        )

    def test_worker_list_requires_login(self):
        response = self.client.get(reverse("task_manager:worker-list"))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('task_manager:worker-list')}"
        )

    def test_search_worker(self):
        self.client.login(username="admin", password="admin123")
        response = self.client.get(reverse("task_manager:worker-list"), {"title": "adm"})
        self.assertContains(response, "admin")


class TaskTypeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.position = Position.objects.create(name="Manager")
        self.user = User.objects.create_superuser(
            username="admin", password="admin123", position=self.position
        )
        self.client.login(username="admin", password="admin123")

    def test_create_task_type(self):
        response = self.client.post(reverse("task_manager:task-type-create"), {"name": "Bug"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TaskType.objects.filter(name="Bug").exists())

    def test_delete_task_type(self):
        task_type = TaskType.objects.create(name="Feature")
        response = self.client.post(reverse("task_manager:task-type-delete", args=[task_type.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TaskType.objects.filter(pk=task_type.pk).exists())
