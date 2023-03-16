from django.test import TestCase
from django.test import Client
from task_manager.labels.models import Labels
from django.urls import reverse

from task_manager.users.models import Users


class StatusesTestCase(TestCase):
    fixtures = ['labels.json', 'users.json']

    def setUp(self):
        self.Client = Client()

    def test_labels_index_view(self):
        test_user = Users.objects.first()

        response = self.client.get(reverse('labels_index'))
        self.assertRedirects(response, reverse('user_login'))

        self.client.force_login(test_user)
        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 2)

    def test_label_create_view(self):
        test_user = Users.objects.first()

        response = self.client.get(reverse('label_create'))
        self.assertRedirects(response, reverse('user_login'))

        response = self.client.post(reverse('label_create'))
        self.assertRedirects(response, reverse('user_login'))

        self.client.force_login(test_user)

        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Labels.objects.count(), 2)

        response = self.client.post(reverse('label_create'), {'name': 'status'})
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Labels.objects.count(), 3)

    def test_label_update_view(self):
        test_user = Users.objects.first()
        test_label = Labels.objects.first()

        response = self.client.get(reverse('label_edit', kwargs={'pk': test_label.id}))
        self.assertRedirects(response, reverse('user_login'))

        response = self.client.post(
            reverse('status_edit', kwargs={'pk': test_label.id}),
            {'name': 'changed_name'}
        )
        self.assertRedirects(response, reverse('user_login'))

        self.client.force_login(test_user)
        response = self.client.get(reverse('label_edit', kwargs={'pk': test_label.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('label_edit', kwargs={'pk': test_label.id}),
            {'name': 'changed_name'}
        )
        test_label.refresh_from_db()
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(test_label.name, 'changed_name')

    def test_label_delete_view(self):
        test_user = Users.objects.first()
        test_label = Labels.objects.first()

        response = self.client.get(reverse('label_destroy', kwargs={'pk': test_label.id}))
        self.assertRedirects(response, reverse('user_login'))

        response = self.client.post(reverse('label_destroy', kwargs={'pk': test_label.id}))
        self.assertRedirects(response, reverse('user_login'))

        self.client.force_login(test_user)

        response = self.client.get(reverse('label_destroy', kwargs={'pk': test_label.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('label_destroy', kwargs={'pk': test_label.id}))
        self.assertEqual(Labels.objects.count(), 1)
        self.assertRedirects(response, reverse('labels_index'))
