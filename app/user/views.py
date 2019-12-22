from user.serializers import (
    UserSerializers,
    AuthtokenSerializers,
)

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

# Create your views here.


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializers


class CreateTokenView(ObtainAuthToken):
    """Create a new token for user"""
    serializer_class = AuthtokenSerializers
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
