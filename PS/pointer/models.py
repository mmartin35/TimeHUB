from django.db import models
from django.contrib.auth.models import User
from intern.models import Intern
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Intern.objects.create(user=instance)

class Timer(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    work_start_morning = models.TimeField(null=True, blank=True)
    work_end_morning = models.TimeField(null=True, blank=True)

    work_start_afternoon = models.TimeField(null=True, blank=True)
    work_end_afternoon = models.TimeField(null=True, blank=True)
