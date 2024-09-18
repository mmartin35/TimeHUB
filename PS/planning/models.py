from django.db import models
from django.contrib.auth.models import User
from intern.models import Intern
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

class Event(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200, default='Initial request')
    request_date = models.DateField(default=timezone.now)
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None)
    duration = models.IntegerField(default=0)
    approved = models.IntegerField(default=0)
    is_archived = models.BooleanField(default=False)
    comment_staff = models.CharField(max_length=200, default='')
