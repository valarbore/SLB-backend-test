# Generated by Django 3.0.3 on 2020-02-16 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainmodules', '0004_auto_20200216_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='best_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='module',
            name='pass_score',
            field=models.FloatField(default=0),
        ),
    ]
