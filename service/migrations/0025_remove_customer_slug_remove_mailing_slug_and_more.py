# Generated by Django 4.2.6 on 2023-10-16 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0024_remove_log_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='mailing',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='message',
            name='slug',
        ),
    ]
