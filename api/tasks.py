from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Task


@shared_task
def check_task_deadlines():
    upcoming_tasks = Task.objects.filter(due_date__gte=timezone.now(), due_date__lte=timezone.now() + timedelta(days=1))
    
    for task in upcoming_tasks:
        send_notification.delay(task.assigned_to.email,task.id,task.title,'reminder')

@shared_task(max_retries=3, default_retry_delay=60)
def send_notification(to_email,task_id,task_title,notification_type='assigned'):
    if notification_type == 'reminder':
        subject = f"Task Deadline Approaching: {task_title}"
        message = f"The task '{task_title}' is due in less than 24 hours. Please complete it as soon as possible."
    elif notification_type == 'assigned':
        subject = 'Task Assignment'
        message = f'A new task has been assigned to you with the id: {task_id}, please check the portal.'
    send_mail(
    recipient_list=[to_email],
    subject=subject,
    message=message,
    fail_silently=False,
    from_email='test@test.com',
)