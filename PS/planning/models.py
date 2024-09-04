from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.title} on {self.date}"
