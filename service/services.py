from datetime import datetime, timedelta
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from service.models import Mailing, Log


NOW_DATE = datetime.now().date()


def change_next_run_mailing(mailing_pk):
    mailing = Mailing.objects.get(pk=mailing_pk)
    if mailing.day:
        mailing.next_run = NOW_DATE + timedelta(days=1)
    elif mailing.week:
        mailing.next_run = NOW_DATE + timedelta(weeks=1)
    elif mailing.month:
        mailing.next_run = NOW_DATE + timedelta(days=30)
    mailing.save()
    return mailing.next_run


def send(pk):
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
    mailing.save()

    mailing.next_run = change_next_run_mailing(mailing.pk)

    Log.objects.create(date_time_last_attempt=datetime.now(), attempt_status=log_status,
                       mail_server_response=server_response,
                       mailing=mailing)
    return mailing.status


