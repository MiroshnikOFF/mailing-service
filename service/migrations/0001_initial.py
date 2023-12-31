# Generated by Django 4.2.5 on 2023-10-04 11:25

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
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=200, verbose_name='Тема письма')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Содержимое письма')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now=True, verbose_name='Дата и время создания')),
                ('start', models.TimeField(default='00:00:00', verbose_name='Время начала рассылки')),
                ('finish', models.TimeField(default='00:00:00', verbose_name='Время окончания рассылки')),
                ('day', models.BooleanField(default=False, verbose_name='Раз в день')),
                ('week', models.BooleanField(default=False, verbose_name='Раз в неделю')),
                ('month', models.BooleanField(default=False, verbose_name='Раз в месяц')),
                ('status', models.CharField(blank=True, max_length=150, null=True, verbose_name='Статус рассылки')),
                ('is_activ', models.BooleanField(default=True, verbose_name='Активная')),
                ('customers', models.ManyToManyField(to='service.customer', verbose_name='Клиенты')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.message', verbose_name='Сообщение')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_last_attempt', models.DateTimeField(auto_now=True, verbose_name='Дата и время последней попытки')),
                ('attempt_status', models.CharField(max_length=150, verbose_name='Статус попытки')),
                ('mail_server_response', models.CharField(max_length=150, verbose_name='Ответ почтового сервера')),
                ('mailing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service.mailing', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
            },
        ),
    ]
