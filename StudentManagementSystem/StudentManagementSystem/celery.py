from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Указываем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentManagementSystem.settings')

# Создаем объект Celery
app = Celery('StudentManagementSystem')

# Загружаем настройки из `settings.py` с префиксом CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
