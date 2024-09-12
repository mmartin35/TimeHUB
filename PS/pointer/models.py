from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from datetime import timedelta, date, time

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Timer.objects.create(user=instance)

class Timer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    work_start_time = models.TimeField(null=True, blank=True)
    work_time_elapsed = models.DurationField(default=timedelta())
    lunch_start_time = models.TimeField(null=True, blank=True)
    lunch_time_elapsed = models.DurationField(default=timedelta())

    class Meta:
        unique_together = ('user', 'date')
