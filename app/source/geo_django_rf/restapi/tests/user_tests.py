from rest_framework import status
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model


class UserCreationTests(APITestCase):
    def __init__(self, methodName='runTest'):
        self.user_base_count = None
        self.User = get_user_model()
        super().__init__(methodName)

    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = self.User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        self.user_base_count = self.User.objects.count()

        # URL for creating an account.
        self.create_url = reverse('user-list')

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }

        response = self.client.post(self.create_url, data, format='json')

        # We want to make sure we have two users in the database..
        self.assertEqual(self.User.objects.count(), self.user_base_count + 1)

        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Additionally, we want to return the username and email upon successful creation.
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

    def test_create_user_with_short_password(self):
        """
        Ensure user is not created for password lengths less than 8.
        """
        data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': 'foo'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.User.objects.count(), self.user_base_count)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        """
        Ensure user is not created without password.
        """
        data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.User.objects.count(), self.user_base_count)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        data = {
            'username': 'foo' + ('o' * 145) + 'bar',
            'email': 'foobarbaz@example.com',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.User.objects.count(), self.user_base_count)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        data = {
            'username': '',
            'email': 'foobarbaz@example.com',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.User.objects.count(), self.user_base_count)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        data = {
            'username': 'testuser',
            'email': 'user@example.com',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.User.objects.count(), self.user_base_count)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        data = {
            'username': 'testuser2',
            'email': 'test@example.com',
            'password': 'testuser'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.User.objects.count(), self.user_base_count)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            'username': 'foobarbaz',
            'email': 'testing',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.User.objects.count(), self.user_base_count)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        data = {
            'username': 'foobar',
            'email': '',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.User.objects.count(), self.user_base_count)
        self.assertEqual(len(response.data['email']), 1)
