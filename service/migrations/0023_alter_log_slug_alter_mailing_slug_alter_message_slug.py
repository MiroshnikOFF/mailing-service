# Generated by Django 4.2.6 on 2023-10-16 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0022_log_slug_mailing_slug_message_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='slug',
            field=models.SlugField(max_length=150, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='slug',
            field=models.SlugField(max_length=150, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='message',
            name='slug',
            field=models.SlugField(max_length=150, unique=True, verbose_name='slug'),
        ),
    ]
