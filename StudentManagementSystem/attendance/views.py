from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework import viewsets
from rest_framework import permissions
from StudentManagementSystem.permissions import IsTeacherOrAdmin
import logging

logger = logging.getLogger(__name__)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeacherOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Attendance.objects.filter(student__user=user)
        return super().get_queryset()
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            logger.info(f"Attendance marked: {response.data['student']} for Course {response.data['course']}")
        return response