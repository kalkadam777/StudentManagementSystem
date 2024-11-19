from django.db import models
from users.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    dob = models.DateField()
    registration_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name