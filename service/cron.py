from datetime import datetime
from django.core.mail import send_mail

from config.settings import EMAIL
from service.models import Service


def send(pk):
    recipient_list = []
    service = Service.objects.get(pk=pk)
    customers = service.customers.all()
    for customer in customers:
        recipient_list.append(customer.email)
    subject = service.message.topic
    message = service.message.body
    send_mail(subject, message, EMAIL, recipient_list)


def send_once_day(pk, start):
    send(pk)


def send_once_week(pk, start, stop):
    if start < datetime.now().time() < stop:
        send(pk)


def send_once_month(pk, start, stop):
    if start < datetime.now().time() < stop:
        send(pk)
