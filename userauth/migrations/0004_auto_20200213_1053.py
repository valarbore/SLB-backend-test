# Generated by Django 3.0.3 on 2020-02-13 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userauth', '0003_auto_20200210_2046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='role',
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_trainer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]