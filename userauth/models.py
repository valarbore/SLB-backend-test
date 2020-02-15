from django.db import models
from django.contrib.auth.models import User
from trainmodules.models import Module
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_trainer = models.BooleanField(default=False)
    avatar = models.CharField(blank=True, max_length=300)
