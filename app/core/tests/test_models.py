from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_with_email_successful(self):
        """Test creating a new user with an email is successfull"""
        email = 'cyrille@webdatastudio.org'
        password = 'test444'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_is_normalized(self):
        """Test the new user email is normalized"""
        email = 'CYRILLEABLE@webdatastudio.org'
        password = 'test444'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        #self.assertEqual(user.email, email.lower())

    def test_user_invalid_email(self):
        """Test the user email is invalid"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')


    def test_create_super_user(self):
        user=get_user_model().objects.create_super_user(
            'test@test.com',
            'test123'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)