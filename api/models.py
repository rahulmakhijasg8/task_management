from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=10)
    due_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")