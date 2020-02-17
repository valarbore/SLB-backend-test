from django.db import models

# Create your models here.
from trainmodules.models import Module, Assignment
from django.contrib.auth.models import User
import datetime


class Performance(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    score = models.FloatField(default=0)
    duration = models.DurationField(default=datetime.timedelta(seconds=0))
