# Generated by Django 4.2.5 on 2023-09-20 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0022_alter_service_finish'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='customer',
        ),
        migrations.AddField(
            model_name='service',
            name='customers',
            field=models.ManyToManyField(to='service.customer'),
        ),
    ]
