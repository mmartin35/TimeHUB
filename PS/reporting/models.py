from django.db import models
from django.utils import timezone

class Report(models.Model):
    name = models.CharField(max_length=50, default='Anonymous', blank=True)
    date = models.DateTimeField(default=timezone.now)
    subject = models.CharField(max_length=100)
    detailed = models.TextField()
    contact = models.CharField(max_length=100, blank=True)
