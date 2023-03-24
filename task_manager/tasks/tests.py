from django.test import TestCase
from django.test import Client
from task_manager.tasks.models import Task
from task_manager.users.models import User
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager import translation
from task_manager.test_form_loader import load_form


class TasksTestCase(TestCase):
    fixtures = ['tasks.json', 'users.json', 'statuses.json', 'labels.json']

    def setUp(self):
        self.Client = Client()
        self.task_form = load_form('task')

    def test_tasks_index_view(self):
        test_user = User.objects.first()

        """ Not authorized user tests """
        response = self.client.get(
            reverse('tasks_index'),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

        """ Authorized user tests """
        self.client.force_login(test_user)
        response = self.client.get(reverse('tasks_index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 2)

    def test_task_create_view(self):
        test_user = User.objects.first()
        test_status = Status.objects.first()

        """ Not authorized user tests """
        response = self.client.get(
            reverse('task_create'),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

        response = self.client.post(
            reverse('task_create'),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

        """ Authorized user tests """
        self.client.force_login(test_user)
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('task_create'),
            self.task_form,
            follow=True,
        )
        self.assertEqual(Task.objects.count(), 3)
        task = Task.objects.last()
        self.assertEqual(task.author, test_user)
        self.assertEqual(task.status, test_status)
        self.assertEqual(task.description, 'new_description')
        self.assertEqual(task.executor, test_user)
        self.assertContains(response, text=translation.TASK_CREATE)

    def test_task_update_view(self):
        test_user = User.objects.first()
        task = Task.objects.first()

        """ Not authorized user tests """
        response = self.client.get(
            reverse('task_edit', kwargs={'pk': task.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

        response = self.client.post(
            reverse('task_edit', kwargs={'pk': task.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

        """ Authorized user tests """
        self.client.force_login(test_user)
        response = self.client.post(
            reverse('task_edit', kwargs={'pk': task.id}),
            self.task_form,
            follow=True,
        )
        task.refresh_from_db()
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(task.name, 'new_task')
        self.assertEqual(task.description, 'new_description')
        self.assertContains(response, text=translation.TASK_UPDATE)

    def test_task_not_authorized_user_delete(self):
        someones_task = Task.objects.last()

        response = self.client.get(
            reverse('task_destroy', kwargs={'pk': someones_task.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

        response = self.client.post(
            reverse('task_destroy', kwargs={'pk': someones_task.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

    def test_task_authorized_user_delete(self):
        task_author = User.objects.last()
        self_task = Task.objects.first()
        someones_task = Task.objects.last()

        self.client.force_login(task_author)

        response = self.client.get(
            reverse('task_destroy', kwargs={'pk': someones_task.id}),
            follow=True
        )
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertContains(response, text=translation.NO_RIGHTS_TO_DELETE_TASK)

        response = self.client.post(
            reverse('task_destroy', kwargs={'pk': someones_task.id}),
            follow=True
        )
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertContains(response, text=translation.NO_RIGHTS_TO_DELETE_TASK)

        response = self.client.get(reverse('task_destroy', kwargs={'pk': self_task.id}))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Task.objects.count(), 2)
        response = self.client.post(
            reverse('task_destroy', kwargs={'pk': self_task.id}),
            follow=True,
        )
        self.assertEqual(Task.objects.count(), 1)
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertContains(response, text=translation.TASK_DELETE)
