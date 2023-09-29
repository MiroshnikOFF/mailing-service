from datetime import datetime
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView

from service.models import Mailing, Customer, Message
from service.cron import send, send_once_day, send_once_week, send_once_month
from config.settings import EMAIL


class HomeTemplateView(TemplateView):
    template_name = 'service/home.html'


class CustomerListView(ListView):
    model = Customer


class CustomerCreateView(CreateView):
    model = Customer
    fields = ('name', 'email', 'comment',)
    success_url = reverse_lazy('service:customers')


class CustomerDetailView(DetailView):
    model = Customer


class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ('name', 'email', 'comment',)

    def get_success_url(self):
        return reverse('service:customer', args=[self.object.pk])


class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('service:customers')


class MessageListView(ListView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = ('topic', 'body',)
    success_url = reverse_lazy('service:messages')


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('topic', 'body')

    def get_success_url(self):
        return reverse('service:message', args=[self.object.id])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('service:messages')


class MailingListView(ListView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    fields = ('customers', 'message', 'start', 'finish', 'day', 'week', 'month',)
    success_url = reverse_lazy('service:services')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = form.save()
        pk = self.object.pk
        if form.is_valid():
            if self.object.start < datetime.now().time() < self.object.finish:
                send(pk)
            else:
                self.object.status = 'создана'
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


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
    fields = ('customers', 'message', 'start', 'finish', 'day', 'week', 'month',)

    def get_success_url(self):
        return reverse('service:mailing', args=[self.object.id])


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('service:mailings')

