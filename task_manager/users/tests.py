from django.test import TestCase
from django.test import Client
from django.urls import reverse

from task_manager.users.models import User
from task_manager import translation
from task_manager.test_form_loader import load_form


class UsersTestCase(TestCase):
    fixtures = ['users.json', 'tasks.json', 'statuses.json', 'labels.json']

    def setUp(self):
        self.client = Client()
        self.user_form = load_form('user')

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
        self.assertContains(response, text=translation.USER_CREATE)

    def test_update_user_success(self):
        current_user = User.objects.first()

        self.client.force_login(current_user)

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
        self.assertContains(response, text=translation.USER_UPDATE)

    def test_update_not_authorized_user(self):
        test_user = User.objects.last()

        response = self.client.get(
            reverse('user_edit', kwargs={'pk': test_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

        response = self.client.post(
            reverse('user_edit', kwargs={'pk': test_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, translation.NOT_AUTHORIZED_USER)

    def test_update_not_own_user(self):
        current_user = User.objects.first()
        test_user = User.objects.last()

        self.client.force_login(current_user)

        response = self.client.get(
            reverse('user_edit', kwargs={'pk': test_user.id}),
            follow=True
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertContains(response, text=translation.NO_RIGHTS_TO_UPDATE_USER)

        response = self.client.post(
            reverse('user_edit', kwargs={'pk': test_user.id}),
            self.user_form,
            follow=True,
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertContains(response, text=translation.NO_RIGHTS_TO_UPDATE_USER)

    def test_delete_not_authorized_user(self):
        test_user = User.objects.last()

        response = self.client.get(
            reverse('user_destroy', kwargs={'pk': test_user.id}),
            follow=True
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

        response = self.client.post(
            reverse('user_destroy', kwargs={'pk': test_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('user_login'))
        self.assertContains(response, text=translation.NOT_AUTHORIZED_USER)

    def test_delete_authorized_user(self):
        current_user = User.objects.first()
        test_user = User.objects.last()

        self.client.force_login(current_user)

        response = self.client.get(
            reverse('user_destroy', kwargs={'pk': test_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertContains(response, text=translation.NO_RIGHTS_TO_DELETE_USER)

        response = self.client.post(
            reverse('user_destroy', kwargs={'pk': test_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertContains(response, text=translation.NO_RIGHTS_TO_DELETE_USER)

        response = self.client.post(
            reverse('user_destroy', kwargs={'pk': current_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertContains(response, text=translation.USER_DELETE)

    def test_delete_protected_user(self):
        protected_user = User.objects.get(id=2)

        self.client.force_login(protected_user)

        response = self.client.get(
            reverse('user_destroy', kwargs={'pk': protected_user.id}),
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('user_destroy', kwargs={'pk': protected_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertContains(response, text=translation.DELETE_PROTECTED_USER)

    def test_login(self):
        get_response = self.client.get('/login/')
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post('/login', {'username': 'andr', 'password': 'secr'})
        self.assertEqual(post_response.status_code, 301)
