from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        Member.objects.create(user=instance)

class Member(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    email   = models.EmailField()
