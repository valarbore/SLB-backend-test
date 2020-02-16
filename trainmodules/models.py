from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)
    decription = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Module(models.Model):
    name = models.CharField(max_length=255, unique=True)
    decription = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    url = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=30, default="Active", choices=[
                              ('Active', 'Active'), ('Inactive', 'Inactive')])
    module_type = models.ForeignKey(
        Type, on_delete=models.SET_NULL, null=True, blank=True)
    privacy = models.CharField(max_length=20, default='Public', choices=[
                               ('Public', 'Public'), ('Private', 'Private')])

    class Meta:
        ordering = ['created']


class Assignment(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name='module_assignment_set')
    trainee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='trainee_assignment_set')
    trainer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='trainer_assignment_set')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='in progress', choices=[
                              ('in progress', 'in progress'), ('completed', 'completed')])

    class Meta:
        unique_together = ('module', 'trainee')
        ordering = ['created']
