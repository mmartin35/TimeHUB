from django.db import models
from django.contrib.auth.models import User
from intern.models import Intern
from django.utils import timezone

class Timer(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    week_number = models.IntegerField(default=timezone.now().isocalendar()[1])
    work_start_morning = models.TimeField(null=True, blank=True)
    work_end_morning = models.TimeField(null=True, blank=True)
    work_start_afternoon = models.TimeField(null=True, blank=True)
    work_end_afternoon = models.TimeField(null=True, blank=True)
