from datetime import datetime

from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView

from config.settings import EMAIL_HOST_USER
from service.forms import CustomerForm, MessageForm, MailingForm
from service.models import Mailing, Customer, Message, Log
from service.cron import send


class HomeTemplateView(TemplateView):
    template_name = 'service/home.html'


class CustomerListView(ListView):
    model = Customer


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('service:customers')


class CustomerDetailView(DetailView):
    model = Customer


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm

    def get_success_url(self):
        return reverse('service:customer', args=[self.object.pk])


class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('service:customers')


class MessageListView(ListView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('service:messages')


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('service:message', args=[self.object.id])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('service:messages')


class MailingListView(ListView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('service:mailings')

    def form_valid(self, form):
        mailing = form.save()
        if mailing.start < datetime.now().time() < mailing.finish:
            mailing.status = 'Запущена'
            customers = mailing.customers.all()
            recipient_list = [customer.email for customer in customers]
            letter = send_mail(mailing.message.topic, mailing.message.body, EMAIL_HOST_USER, recipient_list)
            if letter:
                mailing.status = 'Завершена'
                status = 'Успешно'
                server_response = 'Отправлено'
            else:
                mailing.status = 'Создана'
                status = 'Не успешно'
                server_response = 'Не отправлено'

            Log.objects.create(date_time_last_attempt=datetime.now(), attempt_status=status,
                               mail_server_response=server_response,
                               mailing=mailing)
        else:
            mailing.status = 'Создана'

        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = Mailing.objects.get(pk=self.object.pk)
        customers = service.customers.all()
        context['customers'] = customers
        return context


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('service:mailing', args=[self.object.id])


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('service:mailings')


def get_report(request):
    context = {
        'mailings_done': Mailing.objects.filter(status='Завершена')
    }
    return render(request, 'service/report.html', context=context)


def mailing_off(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    mailing.is_activ = False
    mailing.save()
    context = {
        'object_list': Mailing.objects.all()
    }
    return render(request, 'service/mailing_list.html', context=context)


def mailing_on(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    mailing.is_activ = True
    mailing.save()
    context = {
        'object_list': Mailing.objects.all()
    }
    return render(request, 'service/mailing_list.html', context=context)


class LogListView(ListView):
    model = Log

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(mailing=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        mailing = Mailing.objects.get(pk=self.kwargs.get('pk'))
        context_data['mailing'] = mailing
        return context_data

