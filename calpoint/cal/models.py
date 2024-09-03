from django.db import models
from datetime import timedelta

class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    duration = models.IntegerField(default=1)

    @property
    def end_time(self):
        return self.start_time + timedelta(days=self.duration)

    def __str__(self):
        return self.title
