from django.test import TestCase
from django.test import Client
from task_manager.tasks.models import Tasks
from task_manager.users.models import Users
from django.urls import reverse

from task_manager.statuses.models import Statuses
from task_manager.text import UserFlashMessages, TaskFlashMessages

user_messages = UserFlashMessages()
task_messages = TaskFlashMessages()


class TasksTestCase(TestCase):
    fixtures = ['tasks.json', 'users.json', 'statuses.json', 'labels.json']

    def setUp(self):
        self.Client = Client()
        test_status = Statuses.objects.first()
        test_user = Users.objects.first()
        self.task_form = {
            'name': 'new_task',
            'status': test_status.id,
            'author': test_user.id,
            'description': 'new_description',
            'executor': test_user.id
        }

    def test_tasks_index_view(self):
        test_user = Users.objects.first()

        """ Not authorized user tests """
        response = self.client.get(
            reverse('tasks_index'),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_messages.not_authorhorized_user)

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
        self.assertContains(response, text=user_messages.not_authorhorized_user)

        response = self.client.post(
            reverse('task_create'),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_messages.not_authorhorized_user)

        """ Authorized user tests """
        self.client.force_login(test_user)
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('task_create'),
            self.task_form,
            follow=True,
        )
        self.assertEqual(Tasks.objects.count(), 3)
        task = Tasks.objects.last()
        self.assertEqual(task.author, test_user)
        self.assertEqual(task.status, test_status)
        self.assertEqual(task.description, 'new_description')
        self.assertEqual(task.executor, test_user)
        self.assertContains(response, text=task_messages.create_task)

    def test_task_update_view(self):
        test_user = Users.objects.first()
        task = Tasks.objects.first()

        """ Not authorized user tests """
        response = self.client.get(
            reverse('task_edit', kwargs={'pk': task.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_messages.not_authorhorized_user)

        response = self.client.post(
            reverse('task_edit', kwargs={'pk': task.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_messages.not_authorhorized_user)

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
        self.assertContains(response, text=task_messages.update_task)

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
        self.assertContains(response, text=user_messages.not_authorhorized_user)

        response = self.client.post(
            reverse('task_destroy', kwargs={'pk': someones_task.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_messages.not_authorhorized_user)

        """ Authorized user tests """
        self.client.force_login(task_author)

        response = self.client.get(
            reverse('task_destroy', kwargs={'pk': someones_task.id}),
            follow=True
        )
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertContains(response, text=task_messages.no_rights_to_delete_task)

        response = self.client.post(
            reverse('task_destroy', kwargs={'pk': someones_task.id}),
            follow=True
        )
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertContains(response, text=task_messages.no_rights_to_delete_task)

        response = self.client.get(reverse('task_destroy', kwargs={'pk': self_task.id}))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Tasks.objects.count(), 2)
        response = self.client.post(
            reverse('task_destroy', kwargs={'pk': self_task.id}),
            follow=True,
        )
        self.assertEqual(Tasks.objects.count(), 1)
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertContains(response, text=task_messages.delete_task)
