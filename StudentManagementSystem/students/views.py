
from rest_framework import viewsets, permissions
from .models import Student
from .serializers import StudentSerializer
from StudentManagementSystem.permissions import IsTeacherOrAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from StudentManagementSystem.filter import StudentFilter
from rest_framework.response import Response
from django.core.cache import cache

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
    
    def retrieve(self, request, *args, **kwargs):
        student_id = kwargs['pk']
        cache_key = f'student_profile_{student_id}'
        student = cache.get(cache_key)

        if not student:
            student = Student.objects.get(pk=student_id)
            cache.set(cache_key, student, timeout=3600)

        serializer = self.get_serializer(student)
        return Response(serializer.data)


    def perform_update(self, serializer):
        super().perform_update(serializer)
        student_id = self.kwargs['pk']
        cache_key = f'student_profile_{student_id}'
        cache.delete(cache_key)

