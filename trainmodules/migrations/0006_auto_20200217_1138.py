# Generated by Django 3.0.3 on 2020-02-17 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainmodules', '0005_auto_20200216_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='privacy',
            field=models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], default='Private', max_length=20),
        ),
    ]