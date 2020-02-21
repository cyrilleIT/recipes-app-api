from django.contrib.auth import get_user_model
from core.models import Ingredient
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


def sample_user(email='other@gmail.com', password='password'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)

class PublicIngredientTestAPI(TestCase):
    """Test the publiciy of ingredient"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for list ingredient"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientTestAPI(TestCase):

    def setUp(self):
        self.user = sample_user(email='other2@gmail.com', password='password')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def retrieve_ingredient_test(self):
        """Test retrieving ingredients"""

        Ingredient.objects.create(name='Michoui', user=self.user)
        Ingredient.objects.create(name='Ketchup', user=self.user)

        res = self.client.get(INGREDIENTS_URL)
        data = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(data, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test retrieving connected user list"""

        user_ = sample_user()
        Ingredient.objects.create(name="APF", user=user_)

        Ingredient.objects.create(name="APB", user=self.user)
        Ingredient.objects.create(name="Poulet", user=self.user)

        res = self.client.get(INGREDIENTS_URL)

        self.assertTrue(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_create_ingredient(self):
        """Test create a new ingredient"""

        payload={
            'name':'PainCondiment'
        }

        self.client.post(INGREDIENTS_URL,payload)
        exist = Ingredient.objects.filter(
            name=payload['name'],
            user=self.user
        ).exists()

        self.assertTrue(exist)

    def test_create_invalid_ingredient(self):
        """Test create a new ingredient with invalid data"""

        payload={
            'name':''
        }

        res = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)