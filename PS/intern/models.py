from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Intern(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    arrival = models.DateField(default=timezone.now)
    departure = models.DateField(default=timezone.now)
    is_ongoing = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    days_off_total = models.FloatField(default=25)
    days_off_left = models.FloatField(default=25)
    days_off_onhold = models.FloatField(default=0)
    non_attendance = models.FloatField(default=0)
    mandatory_hours = models.FloatField(default=40)
    total_hours = models.FloatField(default=0)
