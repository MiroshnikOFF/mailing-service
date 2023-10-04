import logging
from datetime import datetime
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from service.models import Mailing, Log

logger = logging.getLogger('main')

NOW_WITHOUT_SECONDS = datetime.now().time().replace(second=0, microsecond=0)


def send(pk):
    mailing = Mailing.objects.get(pk=pk)
    customers = mailing.customers.all()
    recipient_list = [customer.email for customer in customers]

    mailing.status = 'Запущена'
    mailing.save()
    letter = send_mail(mailing.message.topic, mailing.message.body, EMAIL_HOST_USER, recipient_list)
    if letter:
        status = 'Успешно'
        server_response = 'Отправлено'
        mailing.status = 'Завершена'
        mailing.save()
    else:
        status = 'Не успешно'
        server_response = 'Не отправлено'

    Log.objects.create(date_time_last_attempt=datetime.now(), attempt_status=status,
                       mail_server_response=server_response,
                       mailing=mailing)


def send_once_day():
    mailings_once_day = Mailing.objects.filter(status='Создана').filter(is_activ=True).filter(day=True)
    for mailing in mailings_once_day:
        if mailing.start == NOW_WITHOUT_SECONDS:
            send(mailing.pk)


def send_once_week():
    mailings_once_week = Mailing.objects.filter(status='Создана').filter(is_activ=True).filter(week=True)
    for mailing in mailings_once_week:
        if mailing.start == NOW_WITHOUT_SECONDS:
            send(mailing.pk)


def send_once_month():
    mailings_once_month = Mailing.objects.filter(status='Создана').filter(is_activ=True).filter(month=True)
    for mailing in mailings_once_month:
        if mailing.start == NOW_WITHOUT_SECONDS:
            send(mailing.pk)

