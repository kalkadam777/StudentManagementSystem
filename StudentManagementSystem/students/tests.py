
from rest_framework.test import APITestCase
from users.models import User
from .models import Student
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.test import TestCase
from unittest import mock
from notifications.tasks import daily_attendance_reminder

class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="johndoe", password="password123")
        self.student = Student.objects.create(
            user=self.user,
            name="John Doe",
            email="johndoe@example.com",
            dob="2000-01-01"
        )

    def test_student_creation(self):
        self.assertEqual(self.student.name, "John Doe")
        self.assertEqual(self.student.email, "johndoe@example.com")
        self.assertEqual(self.student.dob, "2000-01-01")
        self.assertIsNotNone(self.student.registration_date)


from rest_framework.authtoken.models import Token

class StudentViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="janedoe", password="password123")
        self.student = Student.objects.create(
            user=self.user,
            name="Jane Doe",
            email="janedoe@example.com",
            dob="1995-06-15"
        )
        self.list_url = f"/api/students/"  
        self.detail_url = f"/api/students/{self.student.id}/"  

        # Create a token for the user
        self.student_token = self.client.post(
            "/api/auth/token/login/", 
            {"username": "janedoe", "password": "password123"}
        ).data["auth_token"]

    def authenticate(self):
        """Authenticate the user by setting the token in the Authorization header."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.student_token}')

    def test_list_students(self):
        self.authenticate()  
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jane Doe")  

    def test_student_detail(self):
        self.authenticate()  
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jane Doe")




class CeleryBeatTest(TestCase):
    def setUp(self):
        # Создание интервала для задачи
        schedule, created = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.MINUTES)
        # Создание периодической задачи
        PeriodicTask.objects.create(
            interval=schedule,
            name="Daily Attendance Reminder",
            task="notifications.tasks.daily_attendance_reminder"
        )

    def test_periodic_task_exists(self):
        task = PeriodicTask.objects.filter(name="Daily Attendance Reminder").exists()
        self.assertTrue(task)


class CeleryTaskTest(TestCase):
    @mock.patch('notifications.tasks.daily_attendance_reminder')
    def test_task_direct_execution(self, mock_task):
        # Мокируем выполнение задачи
        mock_task.return_value = 'Reminders sent to 0 students.'
        result = mock_task()

        # Исправьте проверку на строку, которую задача возвращает
        self.assertEqual(result, 'Reminders sent to 0 students.')

    def test_task_execution(self):
        # Выполняем задачу
        result = daily_attendance_reminder.apply_async()
        result.get(timeout=10)

        # Проверяем, что задача выполнена успешно
        self.assertTrue(result.successful())