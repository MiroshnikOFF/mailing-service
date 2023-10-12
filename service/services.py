from datetime import datetime, timedelta

from django.core.cache import cache
from django.core.mail import send_mail

from blog.models import Blog
from config import settings
from config.settings import EMAIL_HOST_USER
from service.models import Mailing, Log, Customer

NOW_DATE = datetime.now().date()


def change_next_run_mailing(mailing_pk: int) -> object:
    """
    Получает рассылку по pk и устанавливает в поле next_run следующую дату запуска исходя из
    установленной периодичности рассылки. Возвращает следующую дату запуска рассылки.
    """

    mailing = Mailing.objects.get(pk=mailing_pk)
    if mailing.day:
        mailing.next_run = NOW_DATE + timedelta(days=1)
    elif mailing.week:
        mailing.next_run = NOW_DATE + timedelta(weeks=1)
    elif mailing.month:
        mailing.next_run = NOW_DATE + timedelta(days=30)
    mailing.save()
    return mailing.next_run


def send_mailing(pk: int) -> str:
    """
    Получает рассылку по pk, формирует список клиентов для рассылки, запускает рассылку.
    В процессе выполнения меняет статус рассылки, сохраняет логи в БД и устанавливает дату следующего запуска.
    Возвращает статус рассылки.
    """

    mailing = Mailing.objects.get(pk=pk)
    customers = mailing.customers.all()
    recipient_list = [customer.email for customer in customers]

    mailing.status = 'Запущена'

    letter = send_mail(mailing.message.topic, mailing.message.body, EMAIL_HOST_USER, recipient_list)
    if letter:
        log_status = 'Успешно'
        server_response = 'Отправлено'
        mailing.status = 'Создана'
    else:
        log_status = 'Не успешно'
        server_response = 'Не отправлено'
    Log.objects.create(date_time_last_attempt=datetime.now(), attempt_status=log_status,
                       mail_server_response=server_response,
                       mailing=mailing)

    mailing.save()
    mailing.next_run = change_next_run_mailing(mailing.pk)
    return mailing.status


def get_count_mailings_all() -> int:
    """Считает количество всех рассылок, кеширует и возвращает результат"""

    count_mailings_all = Mailing.objects.count()
    if settings.CACHE_ENABLED:
        key = 'mailings_all'
        cache_data = cache.get(key)
        if cache_data is None:
            cache_data = count_mailings_all
            cache.set('mailings_all', cache_data)
        return cache_data
    return count_mailings_all


def get_count_mailing_active() -> int:
    """Считает количество активных рассылок, кеширует и возвращает результат"""

    count_mailing_active = get_count_mailings_all() - Mailing.objects.filter(status='Завершена').count()
    if settings.CACHE_ENABLED:
        key = 'mailing_active'
        cache_data = cache.get(key)
        if cache_data is None:
            cache_data = count_mailing_active
            cache.set('mailing_active', cache_data)
        return cache_data
    return count_mailing_active


def get_count_unique_customers() -> int:
    """Считает количество всех уникальных клиентов, кеширует и возвращает результат"""

    count_unique_customers = Customer.objects.values('email').distinct().count()
    if settings.CACHE_ENABLED:
        key = 'unique_customers'
        cache_data = cache.get(key)
        if cache_data is None:
            cache_data = count_unique_customers
            cache.set('unique_customers', cache_data)
        return cache_data
    return count_unique_customers


def get_random_articles_from_cache() -> list[object]:
    """Создает и возвращает queryset из трех случайных статей блога. Кеширует его."""

    queryset = Blog.objects.order_by('?')[:3]
    if settings.CACHE_ENABLED:
        key = 'random_articles'
        cache_data = cache.get(key)
        if cache_data is None:
            cache_data = queryset
            cache.set(key, cache_data)
        return cache_data
    return queryset
