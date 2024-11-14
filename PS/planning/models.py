from django.db import models
from intern.models import Intern
from datetime import datetime

class Event(models.Model):
    intern          = models.ForeignKey(Intern, on_delete=models.CASCADE)
    request_date    = models.DateTimeField(default=datetime.now, null=True, blank=True)

    reason          = models.CharField(max_length=64, default='NA') 
    is_half_day     = models.BooleanField(default=False)
    start_date      = models.DateField(default=None)
    end_date        = models.DateField(default=None)
    duration        = models.FloatField(default=0)

    approbation     = models.IntegerField(default=0)
    comment         = models.CharField(max_length=256, default='No comment given')

class PublicHolidays(models.Model):
    name = models.CharField(max_length=64, default='NA')
    date = models.DateField(default=None)
