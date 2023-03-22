from django.test import TestCase
from django.test import Client
from task_manager.tasks.models import Tasks
from task_manager.users.models import Users
from django.urls import reverse
import json

from task_manager.statuses.models import Statuses
from task_manager import translation
from task_manager import FIXTURE_PATH


task_form = json.load(open(FIXTURE_PATH))['task']


class TasksTestCase(TestCase):
    fixtures = ['tasks.json', 'users.json', 'statuses.json', 'labels.json']

    def setUp(self):
        self.Client = Client()

    def test_tasks_index_view(self):
        test_user = Users.objects.first()

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
        test_user = Users.objects.first()
        test_status = Statuses.objects.first()

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
            task_form,
            follow=True,
        )
        self.assertEqual(Tasks.objects.count(), 3)
        task = Tasks.objects.last()
        self.assertEqual(task.author, test_user)
        self.assertEqual(task.status, test_status)
        self.assertEqual(task.description, 'new_description')
        self.assertEqual(task.executor, test_user)
        self.assertContains(response, text=translation.TASK_CREATE)

    def test_task_update_view(self):
        test_user = Users.objects.first()
        task = Tasks.objects.first()

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
            task_form,
            follow=True,
        )
        task.refresh_from_db()
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(task.name, 'new_task')
        self.assertEqual(task.description, 'new_description')
        self.assertContains(response, text=translation.TASK_UPDATE)

    def test_task_delete_view(self):
        task_author = Users.objects.last()
        self_task = Tasks.objects.first()
        someones_task = Tasks.objects.last()

        """ Not authorized user tests """
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

        """ Authorized user tests """
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

        self.assertEqual(Tasks.objects.count(), 2)
        response = self.client.post(
            reverse('task_destroy', kwargs={'pk': self_task.id}),
            follow=True,
        )
        self.assertEqual(Tasks.objects.count(), 1)
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertContains(response, text=translation.TASK_DELETE)
