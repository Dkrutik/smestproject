# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer
from datetime import datetime, timedelta

class TaskViewTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create a task for testing
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='This is a test task.',
            due_date=datetime.now() + timedelta(days=1),
            status='Pending'
        )

    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'rutikdk',
            'email': 'dk242001@gmail.com',
            'password': 'dike242001'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)

    def test_login_user(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        print("Response status code:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_get_tasks(self):
        url = reverse('task-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_task(self):
        url = reverse('task-list-create')
        data = {
            'title': 'New Task',
            'user':"1",
            'description': 'This is a new task.',
            'due_date': "2024-02-22",
            # (datetime.now() + timedelta(days=2)).isoformat(),
            'status': 'Pending'
        }
        response = self.client.post(url, data, format='json')
        print("Responseaaaaaaaa:", response.status_code)
        print("Response aaaaa:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Task')

    def test_get_task_detail(self):
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_update_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        data = {
            'title': 'Updated Task',
            'status': 'Completed'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.status, 'Completed')

    def test_delete_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
