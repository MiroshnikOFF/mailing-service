# Generated by Django 4.2.6 on 2023-10-16 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0018_alter_mailing_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания'),
        ),
    ]
