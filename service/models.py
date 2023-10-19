from slugify import slugify

from django.db import models
from django.db.utils import IntegrityError

from config import settings

NULLABLE = {'null': True, 'blank': True}


class Customer(models.Model):
    """Модель для работы с клиентами"""

    name = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.EmailField(unique=True, verbose_name='Почта')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')
    slug = models.SlugField(unique=True, verbose_name='slug')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                             verbose_name='Пользователь')

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def save(self, *args, **kwargs):
        """Создает уникальный slug для клиента"""

        self.slug = slugify(self.email)
        base_slug = self.slug
        num = 1
        while Customer.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f'{base_slug}-{num}'
            num += 1
        super().save(*args, **kwargs)


class Message(models.Model):
    """Модель для работы с сообщениями"""

    topic = models.CharField(max_length=200, verbose_name='Тема письма')
    body = models.TextField(**NULLABLE, verbose_name='Содержимое письма')
    slug = models.SlugField(unique=True, verbose_name='slug')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                             verbose_name='Пользователь')

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def save(self, *args, **kwargs):
        """Создает уникальный slug для сообщения"""

        self.slug = slugify(self.topic)
        base_slug = self.slug
        num = 1
        while Message.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f'{base_slug}-{num}'
            num += 1
        super().save(*args, **kwargs)


class Mailing(models.Model):
    """Модель для работы с рассылками"""

    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    start = models.TimeField(default='00:00:00', verbose_name='Время начала рассылки')
    finish = models.TimeField(default='00:00:00', verbose_name='Время окончания рассылки')
    day = models.BooleanField(default=False, verbose_name='Раз в день')
    week = models.BooleanField(default=False, verbose_name='Раз в неделю')
    month = models.BooleanField(default=False, verbose_name='Раз в месяц')
    status = models.CharField(**NULLABLE, max_length=150, verbose_name='Статус рассылки')
    customers = models.ManyToManyField(Customer, verbose_name='Клиенты')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, **NULLABLE, verbose_name='Сообщение')
    is_active = models.BooleanField(default=True, verbose_name='Активная')
    next_run = models.DateField(**NULLABLE, verbose_name='Дата следующей рассылки')
    slug = models.SlugField(unique=True, verbose_name='slug')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                             verbose_name='Пользователь')

    def __str__(self):
        return f"{self.message}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('pk',)
        permissions = [
            (
                'set_is_active_mailing',
                'Can active Рассылка'
            )
        ]

    def save(self, *args, **kwargs):
        """Создает уникальный slug для рассылки"""

        self.slug = slugify(self.message.topic)
        base_slug = self.slug
        num = 1
        while Mailing.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f'{base_slug}-{num}'
            num += 1
        super().save(*args, **kwargs)


class Log(models.Model):
    """Модель для работы с логами рассылок"""

    date_time_last_attempt = models.DateTimeField(auto_now=True, verbose_name='Дата и время последней попытки')
    attempt_status = models.CharField(max_length=150, verbose_name='Статус попытки')
    mail_server_response = models.CharField(max_length=150, verbose_name='Ответ почтового сервера')
    slug = models.SlugField(unique=True, verbose_name='slug')
    mailing = models.ForeignKey(Mailing, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Рассылка')

    def __str__(self):
        return f"{self.date_time_last_attempt} {self.attempt_status}"

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

    def save(self, *args, **kwargs):
        """Создает уникальный slug для лога"""

        self.slug = slugify(self.attempt_status)
        base_slug = self.slug
        num = 1
        while Log.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f'{base_slug}-{num}'
            num += 1
        super().save(*args, **kwargs)
