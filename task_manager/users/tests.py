from django.test import TestCase
from django.test import Client
from task_manager.users.models import Users
from django.urls import reverse


class UsersTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        Users.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        Users.objects.create(username='username1', password='user_password1', first_name='first_name1', last_name='last_name1')
        Users.objects.create(username='username2', password='user_password2', first_name='first_name2', last_name='last_name2')

    def test_users_view(self):
        response = self.client.get(reverse('users_show'))
        self.assertEqual(len(response.context['object_list']), 3)

    def test_create_user(self):
        response = self.client.get('/users/create/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('users_create'),
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
        u = Users.objects.last()

        response = self.client.get(reverse('users_edit', kwargs={'pk': u.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_show'))

        response = self.client.post(
            reverse('users_edit', kwargs={'pk': u.id}),
            {
                'username': 'user_updated',
                'first_name': 'user_update_first_name',
                'last_name': 'user_update_last_name',
                'password1': '123qwe!@#',
                'password2': '123qwe!@#',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_show'))

        self.client.force_login(u)

        response = self.client.get(reverse('users_edit', kwargs={'pk': u.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('users_edit', kwargs={'pk': u.id}),
            {
                'username': 'user_updated',
                'first_name': 'user_update_first_name',
                'last_name': 'user_update_last_name',
                'password1': '123qwe!@#',
                'password2': '123qwe!@#',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_show'))

    def test_delete_user(self):
        response = self.client.get(reverse('users_destroy', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('users_destroy', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 403)

    def test_login(self):
        get_response = self.client.get('/login/')
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post('/login', {'username': 'andr', 'password': 'secr'})
        self.assertEqual(post_response.status_code, 301)
