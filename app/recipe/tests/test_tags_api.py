from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from recipe.serializers import TagSerializer
from core import models

TAGS_URL = reverse('recipe:tag-list')


def sample_user(email='test@test.com',password='tesla'):
    """Create sample user for test"""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicAPIRecipeTest(TestCase):
    """Test API recipe for public user"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that loggin is required for retrieve tags"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPiTests(TestCase):
    """Test API recipe for authorized user"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test creating tags"""
        models.Tag.objects.create(user=self.user,name="Vegan")
        models.Tag.objects.create(user=self.user,name="Dessert")

        res = self.client.get(TAGS_URL)
        tags = models.Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            email='tesla@testapi.com',
            password='testapi'
        )
        models.Tag.objects.create(user=user2, name="Confort")
        tag = models.Tag.objects.create(user=self.user, name="Bio")

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

