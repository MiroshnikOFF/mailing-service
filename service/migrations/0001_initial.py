# Generated by Django 4.2.5 on 2023-09-17 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='ФИО')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Почта')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_last_attempt', models.DateTimeField(auto_now=True, verbose_name='Дата и время последней попытки')),
                ('attempt_status', models.CharField(max_length=150, verbose_name='Статус попытки')),
                ('mail_server_response', models.CharField(max_length=150, verbose_name='Ответ почтового сервера')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=200, verbose_name='Тема письма')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Тело письма')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(verbose_name='Время рассылки')),
                ('periodicity', models.CharField(max_length=50, verbose_name='Периодичность рассылки')),
                ('status', models.CharField(max_length=150, verbose_name='Статус рассылки')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.customer', verbose_name='Клиент')),
                ('log', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.log', verbose_name='Лог')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.message', verbose_name='Сообщение')),
            ],
            options={
                'verbose_name': 'Сервис',
                'verbose_name_plural': 'Сервис',
            },
        ),
    ]
