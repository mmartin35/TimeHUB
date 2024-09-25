from django.db import models
from intern.models import Intern
from django.utils import timezone

class Event(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)

    reason = models.CharField(max_length=64, default='NA') 
    request_date = models.DateField(default=timezone.now)
    half_day = models.IntegerField(default=0)
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=start_date)
    duration = models.FloatField(default=0)

    approbation = models.IntegerField(default=0)
    is_archived = models.BooleanField(default=False)
    staff_comment = models.CharField(max_length=256, default='No comment given')
