from django.test import TestCase
from django.test import Client
from django.urls import reverse

from task_manager.statuses.models import Statuses
from task_manager.users.models import Users
from task_manager.text import UserFlashMessages, StatusFlashMessages


user_messages = UserFlashMessages()
status_messages = StatusFlashMessages()


class StatusesTestCase(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']

    def setUp(self):
        self.Client = Client()
        self.status_form = {'name': 'new_name'}

    def test_statuses_index_view(self):
        test_user = Users.objects.first()

        """ Not authorized user tests """
        response = self.client.get(
            reverse('statuses_index'),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_messages.not_authorhorized_user)

        """ Authorized user tests """
        self.client.force_login(test_user)
        response = self.client.get(reverse('statuses_index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 2)

    def test_status_create_view(self):
        test_user = Users.objects.first()

        """ Not authorized user tests """
        response = self.client.get(
            reverse('status_create'),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_messages.not_authorhorized_user)

        response = self.client.post(
            reverse('status_create'),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_messages.not_authorhorized_user)

        """ Authorized user tests """
        self.client.force_login(test_user)

        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Statuses.objects.count(), 2)

        response = self.client.post(
            reverse('status_create'),
            self.status_form,
            follow=True,
        )
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertEqual(Statuses.objects.count(), 3)
        self.assertContains(response, text=status_messages.create_status)

    def test_status_update_view(self):
        test_user = Users.objects.first()
        test_status = Statuses.objects.first()

        """ Not authorized user """
        response = self.client.get(
            reverse('status_edit', kwargs={'pk': test_status.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_messages.not_authorhorized_user)

        response = self.client.post(
            reverse('status_edit', kwargs={'pk': test_status.id}),
            self.status_form,
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_messages.not_authorhorized_user)

        """ Authorized user tests """
        self.client.force_login(test_user)
        response = self.client.get(reverse('status_edit', kwargs={'pk': test_status.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('status_edit', kwargs={'pk': test_status.id}),
            self.status_form,
            follow=True,
        )
        test_status.refresh_from_db()
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertEqual(test_status.name, 'new_name')
        self.assertContains(response, text=status_messages.update_status)

    def test_status_delete_view(self):
        test_user = Users.objects.first()
        test_status = Statuses.objects.first()

        """ Not authorized user tests """
        response = self.client.get(
            reverse('status_destroy', kwargs={'pk': test_status.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_messages.not_authorhorized_user)

        response = self.client.post(
            reverse('status_destroy', kwargs={'pk': test_status.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_messages.not_authorhorized_user)

        """ Authorized user test """
        self.client.force_login(test_user)

        response = self.client.get(reverse('status_destroy', kwargs={'pk': test_status.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('status_destroy', kwargs={'pk': test_status.id}),
            follow=True,
        )
        self.assertEqual(Statuses.objects.count(), 1)
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertContains(response, text=status_messages.delete_status)

    def test_delete_protected_status(self):
        test_user = Users.objects.first()
        protected_status = Statuses.objects.last()

        self.client.force_login(test_user)
        response = self.client.post(
            reverse('status_destroy', kwargs={'pk': protected_status.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertContains(response, text=status_messages.delete_protected_status)
