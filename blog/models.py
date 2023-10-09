from django.db import models

from config import settings
from service.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    body = models.TextField(**NULLABLE, verbose_name='Содержимое статьи')
    image = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='Изображение')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    published_on = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, **NULLABLE, on_delete=models.SET_NULL, verbose_name='Автор')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
