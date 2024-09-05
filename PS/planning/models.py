from django.db import models
from django.utils import timezone

class Event(models.Model):
    uname = models.CharField(max_length=200, default='Anonymous')
    title = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.title} by {self.uname} on {self.date}'
