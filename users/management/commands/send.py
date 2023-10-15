from django.core.cache import cache

from django.core.management import BaseCommand

from config import settings
from service.models import Mailing
from service.services import send_mailing


def get_mailings():
    """Получает, кеширует и возвращает queryset всех рассылок"""

    mailings = Mailing.objects.all()
    if settings.CACHE_ENABLED:
        key = 'mailings'
        cache_data = cache.get(key)
        if cache_data is None:
            cache_data = mailings
            cache.set(key, cache_data)
        return cache_data
    return mailings


class Command(BaseCommand):
    """Консольная утилита запуска рассылок по команде"""

    def handle(self, *args, **options):
        if get_mailings():
            for mailing in get_mailings():
                print(f'{mailing.pk}  {mailing}')
            while True:
                mailing_pk = input('Введите номер рассылки для запуска либо ENTER для выхода: ')
                if mailing_pk == '':
                    print('GOOD LUCK!')
                    break
                try:
                    mailing = Mailing.objects.get(pk=int(mailing_pk))
                    send_mailing(mailing.pk)
                    print('Готово!')
                    break
                except ValueError:
                    print('Введите цифру!')
                except Mailing.DoesNotExist:
                    print('Не верный номер!')





