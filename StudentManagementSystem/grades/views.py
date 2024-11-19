from .models import Grade
from .serializers import GradeSerializer
from rest_framework import viewsets
from rest_framework import permissions
from StudentManagementSystem.permissions import IsTeacherOrAdmin
import logging

logger = logging.getLogger(__name__)

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeacherOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Grade.objects.filter(student__user=user)
        return super().get_queryset()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            logger.info(f"Grade updated: {response.data['student']} in Course {response.data['course']} with Grade {response.data['grade']}")
        return response
