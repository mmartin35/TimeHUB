from django.db import models
from django.contrib.auth.models import User
from intern.models import Intern
from django.utils import timezone

class Timer(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)

    date = models.DateField(default=timezone.now)
    week_number = models.IntegerField(default=timezone.now().isocalendar()[1])

    working_hours = models.FloatField(default=0)
    t1 = models.TimeField(null=True, blank=True)
    t2 = models.TimeField(null=True, blank=True)
    t3 = models.TimeField(null=True, blank=True)
    t4 = models.TimeField(null=True, blank=True)
