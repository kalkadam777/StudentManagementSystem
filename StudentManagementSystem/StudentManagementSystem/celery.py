from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentManagementSystem.settings')


app = Celery('StudentManagementSystem')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    
app.conf.beat_schedule = {
    'update-popularity-every-day': {
        'task': 'analytics.tasks.update_popularity',
        'schedule': crontab(minute=0, hour=0),  # Каждые сутки
    },
}
