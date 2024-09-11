from django.db import models
from django.utils import timezone

class Report(models.Model):
    date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=50, default='Anonymous', blank=True)
    subject = models.CharField(max_length=100)
    detailed = models.TextField()
    contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.name} - {self.subject}'
