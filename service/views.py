from datetime import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView

from blog.models import Blog
from service.forms import CustomerForm, MessageForm, MailingForm
from service.models import Mailing, Customer, Message, Log
from service.services import send


class HomeTemplateView(TemplateView):
    template_name = 'service/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        count_mailings_all = Mailing.objects.count()
        count_mailing_inactive = Mailing.objects.filter(status='Завершена').count()
        count_mailing_active = count_mailings_all - count_mailing_inactive
        count_unique_customers = Customer.objects.values('email').distinct().count()
        random_articles = Blog.objects.order_by('?')[:3]

        context_data['mailings_all'] = count_mailings_all
        context_data['mailing_active'] = count_mailing_active
        context_data['unique_customers'] = count_unique_customers
        context_data['blog'] = random_articles

        return context_data


class CustomerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'service.view_customer'
    model = Customer

    def get_queryset(self):
        queryset = Customer.objects.filter(user=self.request.user)
        return queryset


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('service:customers')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm

    def get_success_url(self):
        return reverse('service:customer', args=[self.object.pk])


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('service:customers')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return queryset
        queryset = Message.objects.filter(user=user)
        return queryset


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'service.add_message'
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('service:messages')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'service.change_message'
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('service:message', args=[self.object.id])


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'service.delete_message'
    model = Message
    success_url = reverse_lazy('service:messages')


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return queryset
        queryset = Mailing.objects.filter(user=user)
        return queryset


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'service.add_mailing'
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('service:mailings')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()

        mailing = form.save()
        if mailing.start < datetime.now().time() < mailing.finish:
            mailing.status = send(mailing.pk)
        mailing.status = 'Создана'
        mailing.next_run = datetime.now().date()
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = Mailing.objects.get(pk=self.object.pk)
        customers = service.customers.all()
        context['customers'] = customers
        return context


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'service.change_mailing'
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('service:mailing', args=[self.object.id])

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'service.delete_mailing'
    model = Mailing
    success_url = reverse_lazy('service:mailings')


def get_report(request):
    context = {
        'mailings_done': Log.objects.all()
    }
    return render(request, 'service/report.html', context=context)


@login_required
@permission_required('service.set_is_activ_mailing')
def mailing_toggle_activity(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    if mailing.is_active:
        mailing.is_active = False
        mailing.status = 'Завершена'
    else:
        mailing.is_active = True
        mailing.status = 'Создана'
    mailing.save()
    return redirect(reverse_lazy('service:mailings'))


class LogListView(LoginRequiredMixin, ListView):
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
