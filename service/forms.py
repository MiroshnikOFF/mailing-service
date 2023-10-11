from django import forms

from service.models import Customer, Message, Mailing


class StyleFormMixin:
    """Миксин для формирования стиля форм."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CustomerForm(StyleFormMixin, forms.ModelForm):
    """Форма для работы с клиентами"""

    class Meta:
        model = Customer
        exclude = ('user',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    """Форма для работы с сообщениями"""

    class Meta:
        model = Message
        exclude = ('user',)


class MailingForm(StyleFormMixin, forms.ModelForm):
    """Форма для работы с рассылками"""

    class Meta:
        model = Mailing
        exclude = ('status', 'is_active', 'next_run', 'user',)

    def __init__(self, user, *args, **kwargs):
        """
        Переопределяет поля customers и message таким образом, чтобы в них отображались только клиенты и сообщения
        текущего пользователя.
        """

        super().__init__(*args, **kwargs)
        self.fields['customers'].queryset = Customer.objects.filter(user=user)
        self.fields['message'].queryset = Message.objects.filter(user=user)
