from datetime import datetime, timedelta

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView

from service.forms import CustomerForm, MessageForm, MailingForm
from service.models import Mailing, Customer, Message, Log
from service.services import send_mailing, get_random_articles_from_cache, get_count_mailings_all, \
    get_count_mailing_active, get_count_unique_customers


class HomeTemplateView(TemplateView):
    """Контроллер для главной страницы"""

    template_name = 'service/home.html'

    def get_context_data(self, **kwargs) -> dict:
        """
        Собирает в context_data кешированные данные о количестве всех рассылок, активных рассылок, всех уникальных
        клиентов и выбирает 3 случайные статьи из блога, используя сервисные функции, возвращает context_data.
        """

        context_data = super().get_context_data(**kwargs)

        context_data['mailings_all'] = get_count_mailings_all()
        context_data['mailing_active'] = get_count_mailing_active()
        context_data['unique_customers'] = get_count_unique_customers()
        context_data['blog'] = get_random_articles_from_cache()

        return context_data


class CustomerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контроллер для вывода списка клиентов"""

    permission_required = 'service.view_customer'
    model = Customer

    def get_queryset(self) -> list[object]:
        """
        Фильтрует queryset таим образом, чтобы выводились только клиенты текущего пользователя.
        Персоналу позволяет просматривать всех клиентов.
        """

        if self.request.user.is_staff:
            queryset = super().get_queryset()
        else:
            queryset = Customer.objects.filter(user=self.request.user)
        return queryset


class CustomerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер для создания клиента"""

    permission_required = 'service.add_customer'
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('service:customers')

    def form_valid(self, form):
        """Привязывает клиента к текущему пользователю"""

        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class CustomerDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для вывода информации о клиенте"""

    model = Customer


class CustomerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для редактирования клиента"""

    permission_required = 'service.change_customer'
    model = Customer
    form_class = CustomerForm

    def get_success_url(self):
        """Перенаправляет на страницу информации о клиенте"""

        return reverse('service:customer', args=[self.object.pk])


class CustomerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер для удаления клиента"""

    permission_required = 'service.delete_customer'
    model = Customer
    success_url = reverse_lazy('service:customers')


class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контроллер для вывода списка сообщений"""

    permission_required = 'service.view_message'
    model = Message

    def get_queryset(self) -> list[object]:
        """
        Фильтрует queryset таим образом, чтобы выводились только сообщения текущего пользователя.
        Персоналу позволяет просматривать все сообщения.
        """

        queryset = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return queryset
        queryset = Message.objects.filter(user=user)
        return queryset


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер для создания сообщения"""

    permission_required = 'service.add_message'
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('service:messages')

    def form_valid(self, form):
        """Привязывает сообщение к текущему пользователю"""

        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для вывода информации о сообщении"""

    model = Message


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для редактирования сообщения"""

    permission_required = 'service.change_message'
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        """Перенаправляет на страницу информации о сообщении"""

        return reverse('service:message', args=[self.object.id])


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер для удаления сообщения"""

    permission_required = 'service.delete_message'
    model = Message
    success_url = reverse_lazy('service:messages')


class MailingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контроллер для вывода списка рассылок"""

    permission_required = 'service.view_mailing'
    model = Mailing

    def get_queryset(self) -> list[object]:
        """
        Фильтрует queryset таим образом, чтобы выводились только рассылки текущего пользователя.
        Персоналу позволяет просматривать все рассылки.
        """

        queryset = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return queryset
        queryset = Mailing.objects.filter(user=user)
        return queryset


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер для создания рассылки"""

    permission_required = 'service.add_mailing'
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('service:mailings')

    def get_form_kwargs(self):
        """Добавляет в kwargs формы рассылки объект текущего пользователя"""

        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        """
        Привязывает рассылку к текущему пользователю.
        Если текущее время больше времени начала и меньше времени окончания рассылки, запускает рассылку.
        Меняет статус рассылки на "Создана".
        Если создается рассылка со временем старта в будущем, устанавливает дату следующего запуска на следующий день,
        иначе устанавливает текущий день.
        """

        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()

        mailing = form.save()
        if mailing.start < datetime.now().time() < mailing.finish:
            mailing.status = send_mailing(mailing.pk)
        mailing.status = 'Создана'
        if mailing.start > datetime.now().time():
            mailing.next_run = datetime.now().date()
        else:
            mailing.next_run = datetime.now().date() + timedelta(days=1)
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для вывода информации о рассылке"""

    model = Mailing

    def get_context_data(self, **kwargs) -> dict:
        """
        Выбирает рассылку из БД по pk. Создает queryset всех клиентов выбранной рассылки
        и сохраняет его в context_data по ключу 'customers'.
        Возвращает context_data.
        """

        context_data = super().get_context_data(**kwargs)
        service = Mailing.objects.get(pk=self.object.pk)
        customers = service.customers.all()
        context_data['customers'] = customers
        return context_data


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для редактирования рассылки"""

    permission_required = 'service.change_mailing'
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        """Возвращает на страницу вывода информации о рассылке"""

        return reverse('service:mailing', args=[self.object.id])

    def get_form_kwargs(self):
        """Добавляет в kwargs формы рассылки объект текущего пользователя"""

        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер для удаления рассылки"""

    permission_required = 'service.delete_mailing'
    model = Mailing
    success_url = reverse_lazy('service:mailings')


@login_required
def get_report(request):
    """Создает отчет о проведенных рассылках по логам"""

    context = {
        'mailings_done': Log.objects.all()
    }
    return render(request, 'service/report.html', context=context)


@login_required
@permission_required('service.set_is_active_mailing')
def mailing_toggle_activity(request, pk):
    """Включает/отключает рассылку"""

    mailing = Mailing.objects.get(pk=pk)
    if mailing.is_active:
        mailing.is_active = False
        mailing.status = 'Завершена'
    else:
        mailing.is_active = True
        mailing.status = 'Создана'
    mailing.save()
    return redirect('service:mailings')


class LogListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контроллер для вывода списка логов определенной рассылки"""

    permission_required = 'service.view_log'
    model = Log

    def get_queryset(self) -> list[object]:
        """Фильтрует queryset по pk текущей рассылки"""

        queryset = super().get_queryset()
        queryset = queryset.filter(mailing=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs) -> dict:
        """Добавляет в context_data объект текущей рассылки"""

        context_data = super().get_context_data(*args, **kwargs)
        mailing = Mailing.objects.get(pk=self.kwargs.get('pk'))
        context_data['mailing'] = mailing
        return context_data
