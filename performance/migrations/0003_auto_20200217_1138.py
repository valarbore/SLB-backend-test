# Generated by Django 3.0.3 on 2020-02-17 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0002_auto_20200216_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='module',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='user',
        ),
    ]
