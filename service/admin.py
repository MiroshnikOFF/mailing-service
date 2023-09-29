from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from service.models import Customer, Message, Log, Mailing


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('topic', 'body',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('date_time_last_attempt', 'attempt_status', 'mail_server_response',)


@admin.register(Mailing)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('message',)
    filter_vertical = ('customers',)


# class ServiceAdminForm(forms.ModelForm):
#     class Meta:
#         model = Service
#         fields = '__all__'
#         widgets = {
#             'customers': FilteredSelectMultiple(verbose_name='Клиенты', is_stacked=False),
#         }
#
#
# @admin.register(Service)
# class MovieAdmin(admin.ModelAdmin):
#     form = ServiceAdminForm
