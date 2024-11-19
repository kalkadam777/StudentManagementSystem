from django.db import models
from students.models import Student
from courses.models import Course
from users.models import User


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    
    def __str__(self):
        return f"Grade {self.grade} for {self.student.user.username} in {self.course.name}"