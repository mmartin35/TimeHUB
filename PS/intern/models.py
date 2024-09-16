from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Intern.objects.create(user=instance)

class Intern(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_ongoing = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    days_off_total = models.FloatField(default=25)
    days_off_left = models.FloatField(default=25)
