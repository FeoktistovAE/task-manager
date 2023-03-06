from django.test import TestCase
from django.test import Client
from task_manager.tasks.models import Tasks
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from django.urls import reverse


class TasksTestCase(TestCase):
    def setUp(self):
        self.Client = Client()
        user = Users.objects.create_user(
            username='testusername',
            first_name='firstname',
            last_name='lastname',
            password='password',
        )
        Users.objects.create_user(
            username='testusername1',
            first_name='firstname1',
            last_name='lastname1',
            password='password1',
        )
        status = Statuses.objects.create(name='test_status')
        Tasks.objects.create(
            name='test_task1',
            description='test_description',
            author=user,
            executor=user,
            status=status,
        )

    def test_tasks_index_view(self):
        test_user = Users.objects.first()

        response = self.client.get(reverse('tasks_index'))
        self.assertRedirects(response, reverse('user_login'))

        self.client.force_login(test_user)
        response = self.client.get(reverse('tasks_index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)

    def test_task_create_view(self):
        test_user = Users.objects.first()
        test_status = Statuses.objects.first()

        response = self.client.get(reverse('task_create'))
        self.assertRedirects(response, reverse('user_login'))

        response = self.client.post(reverse('task_create'))
        self.assertRedirects(response, reverse('user_login'))

        self.client.force_login(test_user)
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('task_create'),
            {
                'name': 'test_task2',
                'status': test_status.id,
                'author': test_user.id,
                'description': 'test_description',
                'executor': test_user.id
            }
        )
        self.assertEqual(Tasks.objects.count(), 2)
        task = Tasks.objects.last()
        self.assertEqual(task.author, test_user)
        self.assertEqual(task.status, test_status)
        self.assertEqual(task.description, 'test_description')
        self.assertEqual(task.executor, test_user)

    def test_task_update_view(self):
        test_user = Users.objects.first()
        status = Statuses.objects.first()
        task = Tasks.objects.first()

        response = self.client.get(reverse('task_edit', kwargs={'pk': task.id}))
        self.assertRedirects(response, reverse('user_login'))

        response = self.client.post(reverse('task_edit', kwargs={'pk': task.id}))
        self.assertRedirects(response, reverse('user_login'))

        self.client.force_login(test_user)
        response = self.client.post(
            reverse('task_edit', kwargs={'pk': task.id}),
            {
                'name': 'updated name',
                'status': status.id,
                'author': test_user.id,
                'description': 'updated description',
                'executor': test_user.id,
            }
        )
        task.refresh_from_db()
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(task.name, 'updated name')
        self.assertEqual(task.description, 'updated description')

    def test_task_delete_view(self):
        test_user1 = Users.objects.first()
        test_user2 = Users.objects.last()
        task = Tasks.objects.first()

        response = self.client.get(reverse('task_destroy', kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('task_destroy', kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(test_user2)

        response = self.client.get(reverse('task_destroy', kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('task_destroy', kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(test_user1)
        response = self.client.get(reverse('task_destroy', kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Tasks.objects.count(), 1)
        response = self.client.post(reverse('task_destroy', kwargs={'pk': task.id}))
        self.assertEqual(Tasks.objects.count(), 0)
        self.assertRedirects(response, reverse('tasks_index'))
