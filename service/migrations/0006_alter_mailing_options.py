# Generated by Django 4.2.5 on 2023-10-07 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_alter_mailing_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'permissions': [('set_is_activ_mailing', 'Can active mailing')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]