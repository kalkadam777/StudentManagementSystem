from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserActivity, CoursePopularity

class AnalyticsView(APIView):
    def get(self, request):
        user_activity = UserActivity.objects.all().order_by('-total_requests')[:5]
        popular_courses = CoursePopularity.objects.all().order_by('-enrollments')[:5]
        data = {
            'user_activity': [{'user': activity.user.username, 'total_requests': activity.total_requests} for activity in user_activity],
            'popular_courses': [{'course': course.course.name, 'enrollments': course.enrollments} for course in popular_courses]
        }
        return Response(data)
