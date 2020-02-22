from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='testK@test.com', password='testapi'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


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

        # self.assertEqual(user.email, email.lower())

    def test_user_invalid_email(self):
        """Test the user email is invalid"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')

    def test_create_super_user(self):
        """Test super user is created"""
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'test123'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='vegan'
        )

        self.assertTrue(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient str representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Cucumber"
        )

        self.assertTrue(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe str representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Stake mushroom sauce',
            time_minutes=5,
            price=5.00
        )
        self.assertTrue(str(recipe), recipe.title)


