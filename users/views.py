import random

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from config import settings
from users.forms import UserRegisterForm, UserForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save()
        key = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        user.key = key
        send_mail(
            subject='Подтверждение электронной почты',
            message=f'Код для подтверждения: {key}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        group = Group.objects.get(name='user')
        group.user_set.add(user)
        return super().form_valid(form)


class LoginView(BaseLoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_verified:
            return reverse('service:home')
        return reverse('users:verification')


class LogoutView(BaseLogoutView):
    pass


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def email_verification(request):
    if request.method == 'POST':
        input_key = request.POST.get('key')
        try:
            user = User.objects.get(key=input_key)
            user.is_verified = True
            user.save()
        except User.DoesNotExist:
            return render(request, 'users/unsuccessful_verification.html')
        return render(request, 'users/successful_verification.html')
    return render(request, 'users/verification.html')


@login_required
def password_recovery(request):
    if request.method == 'POST':
        new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        input_email = request.POST.get('email')
        try:
            user = User.objects.get(email=input_email)
            user.set_password(new_password)
            user.save()
            send_mail(
                subject='Восстановление доступа',
                message=f'Ваш новый пароль: {new_password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
        except User.DoesNotExist:
            return render(request, 'users/unsuccessful_recovery.html')
        return render(request, 'users/successful_recovery.html')
    return render(request, 'users/password_recovery.html')


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'users.view_user'
    model = User


@login_required
@permission_required('users.set_is_active_user')
def user_toggle_activity(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(reverse_lazy('users:users_list'))
