from django.db import models
from intern.models import Intern
from django.utils import timezone

class DailyTimer(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    worktime = models.FloatField(default=0)
    t1 = models.TimeField(null=True, blank=True)
    t2 = models.TimeField(null=True, blank=True)
    t3 = models.TimeField(null=True, blank=True)
    t4 = models.TimeField(null=True, blank=True)

class ServiceTimer(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    comment = models.CharField(default="NA", max_length=100)

    t1 = models.TimeField(null=True, blank=True)
    t2 = models.TimeField(null=True, blank=True)

class RequestTimer(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
    date = models.DateField(None, blank=True)
    comment = models.CharField(max_length=100)
    approbation = models.IntegerField(default=0)

    original_t1 = models.TimeField(null=True, blank=True)
    original_t2 = models.TimeField(null=True, blank=True)
    original_t3 = models.TimeField(null=True, blank=True)
    original_t4 = models.TimeField(null=True, blank=True)

    altered_t1 = models.TimeField(null=True, blank=True)
    altered_t2 = models.TimeField(null=True, blank=True)
    altered_t3 = models.TimeField(null=True, blank=True)
    altered_t4 = models.TimeField(null=True, blank=True)

class ChangingLog(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
    member = models.CharField(max_length=64)
    date = models.DateField(default=timezone.now)

    original_worktime = models.FloatField(default=0)
    altered_worktime = models.FloatField(default=0)