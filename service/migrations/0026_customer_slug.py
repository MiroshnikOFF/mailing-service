# Generated by Django 4.2.6 on 2023-10-18 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0025_remove_customer_slug_remove_mailing_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='slug'),
        ),
    ]
