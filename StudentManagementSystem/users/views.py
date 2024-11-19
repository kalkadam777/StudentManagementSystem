from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
from rest_framework import permissions
from StudentManagementSystem.permissions import IsAdminUser
import logging
from rest_framework.decorators import action

logger = logging.getLogger('app_logger')


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.AllowAny()]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        response = super().register(request)
        if response.status_code == 201:
            logger.info(f"User registered: {response.data['username']}")
        return response

    @action(detail=False, methods=['post'])
    def login(self, request):
        response = super().login(request)
        if response.status_code == 200:
            logger.info(f"User logged in: {response.data['username']}")
        return response

    @action(detail=False, methods=['post'])
    def logout(self, request):
        response = super().logout(request)
        if response.status_code == 204:
            logger.info("User logged out")
        return response