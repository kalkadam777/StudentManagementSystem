from celery import shared_task
from django.core.mail import send_mail
from datetime import date
from students.models import Student

@shared_task
def daily_attendance_reminder():
    students = Student.objects.all()
    for student in students:
        send_mail(
            'Attendance Reminder',
            'Please remember to mark your attendance for today.',
            'no-reply@school.com',
            [student.email],
        )
    return f'Reminders sent to {students.count()} students.'

@shared_task
def grade_update_notification(student_id):
    student = Student.objects.get(id=student_id)
    send_mail(
        'Grade Update',
        'Your grades have been updated. Please check your profile for details.',
        'no-reply@school.com',
        [student.email],
    )
    return f'Grade update notification sent to {student.email}.'
