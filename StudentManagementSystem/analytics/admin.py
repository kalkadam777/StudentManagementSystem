from django.contrib import admin
from .models import ApiRequest, UserActivity, CoursePopularity

admin.site.register(ApiRequest)
admin.site.register(UserActivity)
admin.site.register(CoursePopularity)
