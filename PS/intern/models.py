from django.db import models
from django.contrib.auth.models import User

class Intern(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.CharField(max_length=15)
    is_ongoing = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    days_off_total = models.FloatField(default=25)
    days_off_left = models.FloatField(default=25)
