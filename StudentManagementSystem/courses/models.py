from django.db import models
from students.models import Student
from users.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE,related_name='courses', limit_choices_to={'role': 'teacher'}, verbose_name="Instructor (Only Teachers)")
    
    def __str__(self):
        return self.name
    
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.name}"
    
    class Meta:
        unique_together = ('student', 'course')