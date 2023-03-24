from django.test import TestCase
from django.test import Client
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager import translation
from task_manager.test_form_loader import load_form


class StatusesTestCase(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']

    def setUp(self):
        self.Client = Client()
        self.status_form = load_form('status')

    def test_statuses_index_view(self):
        test_user = User.objects.first()

        """ Not authorized user tests """
        response = self.client.get(
            reverse('statuses_index'),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

        """ Authorized user tests """
        self.client.force_login(test_user)
        response = self.client.get(reverse('statuses_index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 2)

    def test_status_not_authorized_user_create(self):

        response = self.client.get(
            reverse('status_create'),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

        response = self.client.post(
            reverse('status_create'),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

    def test_status_authorized_user_create(self):
        test_user = User.objects.first()

        self.client.force_login(test_user)

        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), 2)

        response = self.client.post(
            reverse('status_create'),
            self.status_form,
            follow=True,
        )
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertEqual(Status.objects.count(), 3)
        self.assertContains(response, text=translation.STATUS_CREATE)

    def test_status_not_authorized_user_update(self):
        test_status = Status.objects.first()

        response = self.client.get(
            reverse('status_edit', kwargs={'pk': test_status.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

        response = self.client.post(
            reverse('status_edit', kwargs={'pk': test_status.id}),
            self.status_form,
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

    def test_status_authorized_user_update(self):
        test_user = User.objects.first()
        test_status = Status.objects.first()

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
        self.assertContains(response, text=translation.STATUS_UPDATE)

    def test_status_not_authorized_user_delete(self):
        test_status = Status.objects.first()

        """ Not authorized user tests """
        response = self.client.get(
            reverse('status_destroy', kwargs={'pk': test_status.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

        response = self.client.post(
            reverse('status_destroy', kwargs={'pk': test_status.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

    def test_status_authorized_user_delete(self):
        test_user = User.objects.first()
        test_status = Status.objects.first()

        self.client.force_login(test_user)

        response = self.client.get(reverse('status_destroy', kwargs={'pk': test_status.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('status_destroy', kwargs={'pk': test_status.id}),
            follow=True,
        )
        self.assertEqual(Status.objects.count(), 1)
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertContains(response, text=translation.STATUS_DELETE)

    def test_delete_protected_status(self):
        test_user = User.objects.first()
        protected_status = Status.objects.last()

        self.client.force_login(test_user)

        response = self.client.get(
            reverse('status_destroy', kwargs={'pk': protected_status.id}),
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('status_destroy', kwargs={'pk': protected_status.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertContains(response, text=translation.DELETE_PROTECTED_STATUS)
