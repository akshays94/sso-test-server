from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import User
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer

from rest_framework.response import Response

class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class IndexViewset(viewsets.ViewSet):
    
    permission_classes = [AllowAny]

    def list(self, request):
        return Response({ 'message': 'index 1' })


class AttrsViewset(viewsets.ViewSet):
    
    permission_classes = [AllowAny]

    def list(self, request):
        return Response({ 'message': 'attrs 1' })



class MetadataViewset(viewsets.ViewSet):
    
    permission_classes = [AllowAny]

    def list(self, request):
        return Response({ 'message': 'metadata 1' })