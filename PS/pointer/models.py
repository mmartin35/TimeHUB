from django.db import models
from intern.models import Intern
from django.utils import timezone

class Timer(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    working_hours = models.FloatField(default=0)
    t1 = models.TimeField(null=True, blank=True)
    t2 = models.TimeField(null=True, blank=True)
    t3 = models.TimeField(null=True, blank=True)
    t4 = models.TimeField(null=True, blank=True)
    has_service = models.BooleanField(default=False)

class ServiceTimer(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)

    comment = models.CharField(default="NA", max_length=100)
    date = models.DateField(default=timezone.now)
    t1_service = models.TimeField(null=True, blank=True)
    t2_service = models.TimeField(null=True, blank=True)
