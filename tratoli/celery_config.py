from celery import Celery
import os
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tratoli.settings')

app = Celery('tratoli')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_task_deadlines': {
        'task': 'tasks.check_task_deadlines',
        'schedule': crontab(minute=0, hour='*'),
    },
}