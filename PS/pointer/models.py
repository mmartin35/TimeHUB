from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, time

class Timer(models.Model):
    uname = models.CharField(max_length=200, default='Anonymous')
    date = models.DateField(default=timezone.now)
    work_start_time = models.DateTimeField(default=timezone.now)
    work_time_elapsed = models.DurationField(default=timedelta(0))
    lunch_start_time = models.DateTimeField(default=timezone.now)
    lunch_time_elapsed = models.DurationField(default=timedelta(0))

    class Meta:
        unique_together = ('uname', 'date')

    def start_work(self):
        if not self.work_start_time:
            self.work_start_time = timezone.now().time()

    def stop_work(self):
        if self.work_start_time:
            self.work_time_elapsed += timezone.now() - self.work_start_time
            self.work_start_time = None

    def start_lunch(self):
        if not self.lunch_start_time:
            self.lunch_start_time = timezone.now().time()

    def stop_lunch(self):
        if self.lunch_start_time:
            self.lunch_time_elapsed += timezone.now() - self.lunch_start_time
            self.lunch_start_time = None

