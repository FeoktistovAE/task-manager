from django.test import TestCase
from django.test import Client
from task_manager.users.models import Users
from django.urls import reverse


class UsersTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        Users.objects.create_user(username='username', password='password')
        Users.objects.create(
            username='username1',
            password='user_password1',
            first_name='first_name1',
            last_name='last_name1'
        )
        Users.objects.create(
            username='username2',
            password='user_password2',
            first_name='first_name2',
            last_name='last_name2'
        )

    def test_users_view(self):
        response = self.client.get(reverse('users_index'))
        self.assertEqual(len(response.context['object_list']), 3)

    def test_create_user(self):
        response = self.client.get('/users/create/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('user_create'),
            {
                'username': 'create_username',
                'first_name': 'create_first_name',
                'last_name': 'create_last_name',
                'password1': 'Qweasd1!',
                'password2': 'Qweasd1!',
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_update_user(self):
        test_user = Users.objects.last()

        response = self.client.get(reverse('user_edit', kwargs={'pk': test_user.id}))
        self.assertRedirects(response, reverse('users_index'))

        response = self.client.post(
            reverse('user_edit', kwargs={'pk': test_user.id})
        )
        self.assertRedirects(response, reverse('users_index'))

        self.client.force_login(test_user)

        response = self.client.get(reverse('user_edit', kwargs={'pk': test_user.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('user_edit', kwargs={'pk': test_user.id}),
            {
                'username': 'user_updated',
                'first_name': 'updated_firstname',
                'last_name': 'updated_lastname',
                'password1': 'Qwerty123!',
                'password2': 'Qwerty123!',
            }
        )

        test_user.refresh_from_db()
        self.assertEqual(test_user.username, 'user_updated')
        self.assertEqual(test_user.first_name, 'updated_firstname')
        self.assertEqual(test_user.last_name, 'updated_lastname')
        self.assertRedirects(response, reverse('users_index'))

    def test_delete_user(self):
        test_user = Users.objects.last()

        response = self.client.post(reverse('user_destroy', kwargs={'pk': test_user.id}))
        self.assertRedirects(response, reverse('users_index'))

        self.client.force_login(test_user)

        response = self.client.get(reverse('user_destroy', kwargs={'pk': test_user.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('user_destroy', kwargs={'pk': test_user.id}))
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        get_response = self.client.get('/login/')
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post('/login', {'username': 'andr', 'password': 'secr'})
        self.assertEqual(post_response.status_code, 301)
