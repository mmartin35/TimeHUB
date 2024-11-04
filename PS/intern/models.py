from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Intern(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    cns             = models.IntegerField(default=1234567890)
    internship_type = models.CharField(default='NA', max_length=32)
    department      = models.CharField(default='NA', max_length=8)
    tutor           = models.CharField(default='NA', max_length=32)
    mission         = models.CharField(default='NA', max_length=64)

    arrival         = models.DateField(default=timezone.now)
    departure       = models.DateField(default=timezone.now)
    is_ongoing      = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)

    daysoff_total   = models.FloatField(default=0)
    daysoff_left    = models.FloatField(default=0)
    daysoff_onhold  = models.FloatField(default=0)

    non_attendance  = models.FloatField(default=0)
    mandatory_hours = models.FloatField(default=0)
    total_hours     = models.FloatField(default=0)
    regime          = models.IntegerField(default=100)