from django.test import TestCase
from django.test import Client
from task_manager.labels.models import Labels
from django.urls import reverse
import json

from task_manager.users.models import Users
from task_manager import translation
from task_manager import FIXTURE_PATH


label_form = json.load(open(FIXTURE_PATH))['label']


class LabelsTestCase(TestCase):
    fixtures = ['labels.json', 'users.json', 'tasks.json', 'statuses.json']

    def setUp(self):
        self.Client = Client()

    def test_labels_index_view(self):
        test_user = Users.objects.first()

        """Not authorized user tests"""
        response = self.client.get(
            reverse('labels_index'),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

        self.client.force_login(test_user)
        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 2)

    def test_label_create_view(self):
        test_user = Users.objects.first()

        """ Not authorized user tests"""
        response = self.client.get(reverse('label_create'))
        self.assertRedirects(response, reverse('user_login'))

        response = self.client.post(reverse('label_create'))
        self.assertRedirects(response, reverse('user_login'))

        """ Authorized user tests"""
        self.client.force_login(test_user)

        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Labels.objects.count(), 2)

        response = self.client.post(
            reverse('label_create'),
            label_form,
            follow=True,
        )
        created_label = Labels.objects.last()
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Labels.objects.count(), 3)
        self.assertEqual(created_label.name, 'new_name')
        self.assertContains(response, text=translation.LABEL_CREATE)

    def test_label_update_view(self):
        test_user = Users.objects.first()
        test_label = Labels.objects.first()

        """ Not authorized user tests """
        response = self.client.get(
            reverse('label_edit', kwargs={'pk': test_label.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, translation.NOT_AUTHORIZED_USER)

        response = self.client.post(
            reverse('status_edit', kwargs={'pk': test_label.id}),
            label_form,
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, translation.NOT_AUTHORIZED_USER)

        """ Authorized user tests """
        self.client.force_login(test_user)
        response = self.client.get(reverse('label_edit', kwargs={'pk': test_label.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('label_edit', kwargs={'pk': test_label.id}),
            label_form,
            follow=True,
        )
        test_label.refresh_from_db()
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(test_label.name, 'new_name')
        self.assertContains(response, translation.LABEL_UPDATE)

    def test_label_delete_view(self):
        test_user = Users.objects.first()
        test_label = Labels.objects.first()

        """" Not authorized user tests """
        response = self.client.get(
            reverse('label_destroy', kwargs={'pk': test_label.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

        response = self.client.post(
            reverse('label_destroy', kwargs={'pk': test_label.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

        """ Authorized user tests """
        self.client.force_login(test_user)

        response = self.client.get(reverse('label_destroy', kwargs={'pk': test_label.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('label_destroy', kwargs={'pk': test_label.id}),
            follow=True,
        )
        self.assertEqual(Labels.objects.count(), 1)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertContains(response, text=translation.LABEL_DELETE)

    def test_delete_protected_label(self):
        test_user = Users.objects.first()
        protected_label = Labels.objects.last()

        self.client.force_login(test_user)
        response = self.client.get(
            reverse('label_destroy', kwargs={'pk': protected_label.id}),
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('label_destroy', kwargs={'pk': protected_label.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('labels_index'))
        self.assertContains(response, text=translation.DELETE_PROTECTED_LABEL)
