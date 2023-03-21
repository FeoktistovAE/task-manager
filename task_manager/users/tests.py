from django.test import TestCase
from django.test import Client
from django.urls import reverse

from task_manager.users.models import Users
from task_manager.text import UserFlashMessages

user_flash_messages = UserFlashMessages()


class UsersTestCase(TestCase):
    fixtures = ['users.json', 'tasks.json', 'statuses.json', 'labels.json']

    def setUp(self):
        self.client = Client()
        self.user_form = {
            'username': 'new_username',
            'first_name': 'new_firstname',
            'last_name': 'new_lastname',
            'password1': 'Qweasd1!',
            'password2': 'Qweasd1!',
        }

    def test_users_view(self):
        response = self.client.get(reverse('users_index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 3)

    def test_create_user(self):
        response = self.client.get('/users/create/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('user_create'),
            self.user_form,
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_flash_messages.create_user)

    def test_update_user(self):
        current_user = Users.objects.first()
        test_user = Users.objects.last()

        """ Not authorized user tests """
        response = self.client.get(
            reverse('user_edit', kwargs={'pk': test_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_flash_messages.not_authorhorized_user)

        response = self.client.post(
            reverse('user_edit', kwargs={'pk': test_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, user_flash_messages.not_authorhorized_user)

        """ Authorized user tests """
        self.client.force_login(current_user)
        response = self.client.get(
            reverse('user_edit', kwargs={'pk': test_user.id}),
            follow=True
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertContains(response, text=user_flash_messages.no_rights_to_update_user)

        response = self.client.post(
            reverse('user_edit', kwargs={'pk': test_user.id}),
            self.user_form,
            follow=True,
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertContains(response, text=user_flash_messages.no_rights_to_update_user)

        response = self.client.get(reverse('user_edit', kwargs={'pk': current_user.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('user_edit', kwargs={'pk': current_user.id}),
            self.user_form,
            follow=True,
        )
        current_user.refresh_from_db()
        self.assertEqual(current_user.username, 'new_username')
        self.assertEqual(current_user.first_name, 'new_firstname')
        self.assertEqual(current_user.last_name, 'new_lastname')
        self.assertRedirects(response, reverse('users_index'))
        self.assertContains(response, text=user_flash_messages.update_user)

    def test_delete_user(self):
        current_user = Users.objects.first()
        test_user = Users.objects.last()

        """ Not authorized user tests """
        response = self.client.get(
            reverse('user_destroy', kwargs={'pk': test_user.id}),
            follow=True
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_flash_messages.not_authorhorized_user)

        response = self.client.post(
            reverse('user_destroy', kwargs={'pk': test_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=user_flash_messages.not_authorhorized_user)

        """ Authorized user tests """
        self.client.force_login(current_user)

        response = self.client.get(
            reverse('user_destroy', kwargs={'pk': test_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertContains(response, text=user_flash_messages.no_rights_to_delete_user)

        response = self.client.post(
            reverse('user_destroy', kwargs={'pk': test_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertContains(response, text=user_flash_messages.no_rights_to_delete_user)

        response = self.client.post(
            reverse('user_destroy', kwargs={'pk': current_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertContains(response, text=user_flash_messages.delete_user)

    def test_delete_protected_user(self):
        protected_user = Users.objects.get(id=2)
        self.client.force_login(protected_user)
        response = self.client.post(
            reverse('user_destroy', kwargs={'pk': protected_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertContains(response, text=user_flash_messages.delete_protected_user)

    def test_login(self):
        get_response = self.client.get('/login/')
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post('/login', {'username': 'andr', 'password': 'secr'})
        self.assertEqual(post_response.status_code, 301)
