from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from datetime import timedelta, time

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Timer.objects.create(user=instance)

class Timer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    work_start_time = models.DateTimeField(default=timezone.now)
    work_time_elapsed = models.DurationField(default=timedelta(0))
    lunch_start_time = models.DateTimeField(default=timezone.now)
    lunch_time_elapsed = models.DurationField(default=timedelta(0))

    class Meta:
        unique_together = ('user', 'date')

    def start_work(self):
        if not self.work_start_time:
            self.work_start_time = timezone.now().time()

    def stop_work(self):
        if self.work_start_time:
            self.work_time_elapsed += timezone.now() - self.work_start_time
            self.work_start_time = None

    def start_lunch(self):
        if not self.lunch_start_time:
            self.lunch_start_time = timezone.now().time()

    def stop_lunch(self):
        if self.lunch_start_time:
            self.lunch_time_elapsed += timezone.now() - self.lunch_start_time
            self.lunch_start_time = None

    def __str__(self):
        return f'{self.user} - {self.date} (Started at {self.work_start_time})- {self.work_time_elapsed} + {self.lunch_time_elapsed}'
