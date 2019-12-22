from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicAPIUserTests(TestCase):
    """Test the user API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test create user with valid payload is successfull"""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'test',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """Test creating a user that already exist"""
        payload = {
            'email': 'test@test.com',
            'password': 'test',
            'name': 'test'
        }
        # user creation with payload data
        create_user(**payload)

        # user creation with post with also payload data
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test creating a user with a short password < 5 characters"""
        payload = {
            'email': 'test@test.com',
            'password': 'pw',
            'name': 'test'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        )

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test create token if user is valid"""
        payload = {
            'email': 'test@test.com',
            'password': 'tesla2',
            'name': 'test'
        }

        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertTrue(res.status_code, status.HTTP_200_OK)

    def test_create_token_with_invalid_credentials(self):
        """Test token is not created if credentials is invalid"""
        create_user(email='test@test.com', password='password', name='test')
        payload = {
            'email': 'test@test.com',
            'password': 'wrong',
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_no_user(self):
        """Test token is not created if user not exist"""
        payload = {
            'email': 'test@test.com',
            'password': 'pw',
            'name': 'test'
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test token is not created if field is missing"""
        res = self.client.post(TOKEN_URL,
                               {'email': 'test@test.com', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
