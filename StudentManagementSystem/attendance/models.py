from django.db import models
from students.models import Student
from courses.models import Course

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()  # Дата занятия
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')

    def __str__(self):
        return f"{self.student.user.username} - {self.get_status_display()} on {self.date} in {self.course.name}"

    class Meta:
        unique_together = ('student', 'course', 'date')  # Уникальная запись на день
