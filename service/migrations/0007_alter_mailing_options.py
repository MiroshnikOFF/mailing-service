# Generated by Django 4.2.5 on 2023-10-07 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_alter_mailing_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'permissions': [('set_is_active_mailing', 'Can active mailing')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]
