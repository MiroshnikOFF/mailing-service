from django import forms

from service.models import Customer, Message, Mailing


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CustomerForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Customer
        exclude = ('user',)


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        exclude = ('user',)


class MailingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        exclude = ('status', 'is_active', 'next_run', 'user',)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customers'].queryset = Customer.objects.filter(user=user)
        self.fields['message'].queryset = Message.objects.filter(user=user)
