from django_filters import rest_framework as filters
from students.models import Student
from courses.models import Course

class CourseFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')  # Case-insensitive filter for course name
    instructor = filters.CharFilter(field_name='instructor__username', lookup_expr='icontains')

    class Meta:
        model = Course
        fields = ['name', 'instructor']  # Fields to filter

class StudentFilter(filters.FilterSet):
    username = filters.CharFilter(field_name='user__username', lookup_expr='icontains')  # Filter by user.username
    email = filters.CharFilter(field_name='user__email', lookup_expr='icontains')  # Filter by email

    class Meta:
        model = Student
        fields = ['username', 'email']  # Fields to filter
