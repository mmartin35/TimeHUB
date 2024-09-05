from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Timer(models.Model):
    uname = models.CharField(max_length=200, default='Anonymous')
    date = models.DateField(default=timezone.now)
    work_start_time = models.TimeField(null=True, blank=True)
    work_time_elapsed = models.DurationField(null=True, blank=True)
    lunch_start_time = models.TimeField(null=True, blank=True)
    lunch_time_elapsed = models.DurationField(null=True, blank=True)

    class Meta:
        unique_together = ('uname', 'date')

    def start_work(self):
        if not self.work_start_time:
            self.work_start_time = timezone.now()

    def stop_work(self):
        if self.work_start_time:
            self.work_time_elapsed += timezone.now() - self.work_start_time
            self.work_start_time = None

    def start_lunch(self):
        if not self.lunch_start_time:
            self.lunch_start_time = timezone.now()

    def stop_lunch(self):
        if self.lunch_start_time:
            self.lunch_time_elapsed += timezone.now() - self.lunch_start_time
            self.lunch_start_time = None
