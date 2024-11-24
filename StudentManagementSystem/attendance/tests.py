from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from courses.models import Course
from attendance.models import Attendance
from students.models import Student

class AttendanceAPITests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            email="teacher@example.com",
            password="password123",
            role="teacher",
            username="teacher_user"  
        )

        self.student_user = User.objects.create_user(
            email="student@example.com",
            password="password123",
            role="student",
            username="student_user" 
        )

        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="admin123",
            role="admin",
            username="admin_user"  
        )

        self.course = Course.objects.create(
            name="Physics",
            description="Physics Course",
            instructor=self.teacher
        )
        
        self.student = Student.objects.create(user=self.student_user)
     
        self.attendance = Attendance.objects.create(
            student=self.student,
            course=self.course,
            date="2024-11-20",
            status="present"
        )
        


        # Получение токенов через Djoser
        self.teacher_token = self.client.post(
            "/api/auth/token/login/", 
            {"username": "teacher_user", "password": "password123"}
        ).data["auth_token"]

        self.student_token = self.client.post(
            "/api/auth/token/login/", 
            {"username": "student_user", "password": "password123"}
        ).data["auth_token"]

        self.admin_token = self.client.post(
            "/api/auth/token/login/", 
            {"username": "admin_user", "password": "admin123"}
        ).data["auth_token"]

    def test_teacher_can_mark_attendance(self):
        """Тест на возможность учителя отмечать посещаемость."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token}")
        response = self.client.post("/api/attendance/", {
            "student": self.student.id,
            "course": self.course.id,
            "date": "2024-11-19", 
            "status": "present"
        })
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_can_view_own_attendance(self):
        """Тест на возможность студента просматривать свою посещаемость."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.student_token}")
        response = self.client.get(f"/api/attendance/{self.attendance.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "present")

    def test_admin_can_view_all_attendance(self):
        """Тест на возможность администратора просматривать все записи посещаемости."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token}")
        response = self.client.get("/api/attendance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)