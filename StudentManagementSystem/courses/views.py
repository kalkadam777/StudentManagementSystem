from rest_framework import viewsets
from .models import Course,Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from rest_framework import permissions
from StudentManagementSystem.permissions import IsTeacherOrAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from StudentManagementSystem.filter import CourseFilter
from drf_spectacular.utils import extend_schema, extend_schema_view
import logging

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        description="Получить список всех курсов.",
        responses={200: CourseSerializer(many=True)},
    ),
    retrieve=extend_schema(
        description="Получить детали конкретного курса.",
        responses={200: CourseSerializer},
    ),
)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CourseFilter
    ordering_fields = ['name', 'instructor']  # Allow ordering by these fields
    ordering = ['name']  # Default ordering
    
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeacherOrAdmin()]
        return [permissions.IsAuthenticated()]
    
    
    
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeacherOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Enrollment.objects.filter(student__user=user)
        return super().get_queryset()
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            logger.info(f"Enrollment created: Student ID {response.data['student']} in Course ID {response.data['course']}")
        return response
