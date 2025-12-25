from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('ANALYST', 'Analyst'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


class Event(models.Model):
    SEVERITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    )

    source_name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} - {self.severity}"


class Alert(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('ACK', 'Acknowledged'),
        ('RESOLVED', 'Resolved'),
    )

    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.event.event_type}"
