# Generated by Django 4.2.5 on 2023-10-06 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_alter_mailing_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'permissions': [('change_is_activ', 'Can activ mailing')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]
