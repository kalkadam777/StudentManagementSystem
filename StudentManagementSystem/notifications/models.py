from django.db import models
from users.models import User

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  # Получатель
    message = models.TextField()  # Сообщение
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    is_read = models.BooleanField(default=False)  # Статус прочтения

    def __str__(self):
        return f"Notification for {self.recipient.username} - {'Read' if self.is_read else 'Unread'}"
