from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Event.objects.create(user=instance)

class Event(models.Model):
    user = models.CharField(default='Anonymous', max_length=50)
    reason = models.CharField(max_length=200)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    half_day = models.IntegerField(default=0)
    approved = models.BooleanField(default=False)
    remaining_days = models.FloatField(default=25)

    def __str__(self):
        return f'{self.user} -> {self.reason} between {self.start_date} and {self.end_date} | status: {self.approved}'
