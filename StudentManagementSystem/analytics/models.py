from django.db import models

from courses.models import Course  
from django.conf import settings

class ApiRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10) 

    def __str__(self):
        return f"Request by {self.user.username} to {self.endpoint}"

class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login_timestamp = models.DateTimeField(auto_now_add=True)
    last_request_timestamp = models.DateTimeField(auto_now=True)
    total_requests = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Activity of {self.user.username}"

class CoursePopularity(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='popularity')
    views = models.PositiveIntegerField(default=0)
    enrollments = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.course.name} popularity"
