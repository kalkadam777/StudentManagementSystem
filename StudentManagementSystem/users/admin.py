from django.contrib import admin
from .models import *
from grades.models import Grade
from students.models import Student
from courses.models import Course
from notifications.models import Notification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
admin.site.register(Grade)
admin.site.register(Student)    
admin.site.register(Course)
admin.site.register(Notification)