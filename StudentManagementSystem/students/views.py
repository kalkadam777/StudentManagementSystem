
from rest_framework import viewsets, permissions
from .models import Student
from .serializers import StudentSerializer
from StudentManagementSystem.permissions import IsTeacherOrAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from StudentManagementSystem.filter import StudentFilter

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = StudentFilter
    ordering_fields = ['user__username', 'user__email']  # Allow ordering by these fields
    ordering = ['user__username']  # Default ordering
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeacherOrAdmin()]
        elif self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Student.objects.none() 
        if user.role == 'student':
            return Student.objects.filter(user=user)
        return super().get_queryset()

