from django.test import TestCase
from django.test import Client
from task_manager.labels.models import Labels
from django.urls import reverse

from task_manager.users.models import Users
from task_manager.text import UserFlashMessages, LabelFlashMessages


user_messages = UserFlashMessages()
label_messages = LabelFlashMessages()


class LabelsTestCase(TestCase):
    fixtures = ['labels.json', 'users.json', 'tasks.json', 'statuses.json']

    def setUp(self):
        self.Client = Client()
        self.label_form = {'name': 'new_name'}

    def test_labels_index_view(self):
        test_user = Users.objects.first()

        """Not authorized user tests"""
        response = self.client.get(
            reverse('labels_index'),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_messages.not_authorhorized_user)

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
            self.label_form,
            follow=True,
        )
        created_label = Labels.objects.last()
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Labels.objects.count(), 3)
        self.assertEqual(created_label.name, 'new_name')
        self.assertContains(response, text=label_messages.create_label)

    def test_label_update_view(self):
        test_user = Users.objects.first()
        test_label = Labels.objects.first()

        """ Not authorized user tests """
        response = self.client.get(
            reverse('label_edit', kwargs={'pk': test_label.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, user_messages.not_authorhorized_user)

        response = self.client.post(
            reverse('status_edit', kwargs={'pk': test_label.id}),
            self.label_form,
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, user_messages.not_authorhorized_user)

        """ Authorized user tests """
        self.client.force_login(test_user)
        response = self.client.get(reverse('label_edit', kwargs={'pk': test_label.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('label_edit', kwargs={'pk': test_label.id}),
            self.label_form,
            follow=True,
        )
        test_label.refresh_from_db()
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(test_label.name, 'new_name')
        self.assertContains(response, label_messages.update_label)

    def test_label_delete_view(self):
        test_user = Users.objects.first()
        test_label = Labels.objects.first()

        """" Not authorized user tests """
        response = self.client.get(
            reverse('label_destroy', kwargs={'pk': test_label.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_messages.not_authorhorized_user)

        response = self.client.post(
            reverse('label_destroy', kwargs={'pk': test_label.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_messages.not_authorhorized_user)

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
        self.assertContains(response, text=label_messages.delete_label)

    def test_delete_protected_label(self):
        test_user = Users.objects.first()
        protected_label = Labels.objects.last()

        self.client.force_login(test_user)
        response = self.client.post(
            reverse('label_destroy', kwargs={'pk': protected_label.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('labels_index'))
        self.assertContains(response, text=label_messages.delete_protected_label)
