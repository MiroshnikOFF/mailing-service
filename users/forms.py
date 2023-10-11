from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from service.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма для регистрации пользователей"""

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserForm(StyleFormMixin, UserChangeForm):
    """Форма для редактирования пользователей"""

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        """Удаление поля 'password' из формы"""

        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
