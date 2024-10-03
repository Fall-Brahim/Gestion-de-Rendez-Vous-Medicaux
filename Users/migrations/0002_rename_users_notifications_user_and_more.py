# Generated by Django 5.0.6 on 2024-05-23 17:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifications',
            old_name='users',
            new_name='user',
        ),
        migrations.AddField(
            model_name='notifications',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='notifications',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
