import logging
from datetime import datetime
from django.core.mail import send_mail

from config.settings import EMAIL
from service.models import Mailing




def send(pk):
    recipient_list = []
    mailing = Mailing.objects.get(pk=pk)
    customers = mailing.customers.all()
    for customer in customers:
        customer.status = 'завершена'
        recipient_list.append(customer.email)
    subject = mailing.message.topic
    message = mailing.message.body
    send_mail(subject, message, EMAIL, recipient_list)


def send_once_day():
    # recipient_list = []
    mailing = Mailing.objects.get(pk=33)
    # customers = mailing.customers.all()
    # for customer in customers:
    #     customer.status = 'завершена'
    #     recipient_list.append(customer.email)
    # subject = 'bla bla bla'
    # message = 'mmmmmmeeeeeeessssssaaaaaggggggeeeeee'
    # send_mail(subject, message, EMAIL, ['taxi8308@mail.ru'])
    # print('HI!')
    # mailings = Mailing.objects.all()
    # for mailing in mailings:
    #     send(mailing.pk)

    with open('/Users/miroshnikoff/PycharmProjects/mailing-service/service/temp.txt', 'a') as file:
        file.write(mailing.pk)
    logger = logging.getLogger('main')
    logger.debug('запись в файл')




def send_once_week(pk, start):
    if start == datetime.now().time():
        send(pk)


def send_once_month(pk, start):
    if start == datetime.now().time():
        send(pk)
