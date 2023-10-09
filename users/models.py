from django.contrib.auth.models import AbstractUser
from django.db import models

from service.models import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    key = models.CharField(max_length=12, verbose_name='Ключ для верификации почты', **NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='Почта верифицирована')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            (
                'set_is_active_user',
                'Can active user'
            )
        ]



