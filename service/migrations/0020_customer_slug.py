# Generated by Django 4.2.6 on 2023-10-16 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0019_alter_mailing_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, null=True, verbose_name='slug'),
        ),
    ]