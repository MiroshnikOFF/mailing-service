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
        fields = '__all__'


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = '__all__'


class MailingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        exclude = ('status', 'is_activ',)
