from django.test import TestCase
from django.test import Client
from task_manager.statuses.models import Statuses
from task_manager.users.models import Users
from django.urls import reverse


class StatusesTestCase(TestCase):
    def setUp(self):
        self.Client = Client()
        Users.objects.create_user(username='username', password='password')
        Statuses.objects.create(name='test_status1')
        Statuses.objects.create(name='test_status2')

    def test_statuses_index_view(self):
        test_user = Users.objects.first()

        response = self.client.get(reverse('statuses_index'))
        self.assertRedirects(response, reverse('user_login'))

        self.client.force_login(test_user)
        response = self.client.get(reverse('statuses_index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 2)

    def test_status_create_view(self):
        test_user = Users.objects.first()

        response = self.client.get(reverse('status_create'))
        self.assertRedirects(response, reverse('user_login'))

        response = self.client.post(reverse('status_create'))
        self.assertRedirects(response, reverse('user_login'))

        self.client.force_login(test_user)

        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Statuses.objects.count(), 2)

        response = self.client.post(reverse('status_create'), {'name': 'status'})
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertEqual(Statuses.objects.count(), 3)

    def test_status_update_view(self):
        test_user = Users.objects.first()
        test_status = Statuses.objects.first()

        response = self.client.get(reverse('status_edit', kwargs={'pk': test_status.id}))
        self.assertRedirects(response, reverse('user_login'))

        response = self.client.post(
            reverse('status_edit', kwargs={'pk': test_status.id}),
            {'name': 'changed_name'}
        )
        self.assertRedirects(response, reverse('user_login'))

        self.client.force_login(test_user)
        response = self.client.get(reverse('status_edit', kwargs={'pk': test_status.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('status_edit', kwargs={'pk': test_status.id}),
            {'name': 'changed_name'}
        )
        test_status.refresh_from_db()
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertEqual(test_status.name, 'changed_name')

    def test_status_delete_view(self):
        test_user = Users.objects.first()
        test_status = Statuses.objects.first()

        response = self.client.get(reverse('status_destroy', kwargs={'pk': test_status.id}))
        self.assertRedirects(response, reverse('user_login'))

        response = self.client.post(reverse('status_destroy', kwargs={'pk': test_status.id}))
        self.assertRedirects(response, reverse('user_login'))

        self.client.force_login(test_user)

        response = self.client.get(reverse('status_destroy', kwargs={'pk': test_status.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('status_destroy', kwargs={'pk': test_status.id}))
        self.assertEqual(Statuses.objects.count(), 1)
        self.assertRedirects(response, reverse('statuses_index'))
