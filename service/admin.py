from django.contrib import admin

from service.models import Customer, Message, Log, Mailing


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('topic', 'body',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('date_time_last_attempt', 'attempt_status', 'mail_server_response', 'mailing',)


@admin.register(Mailing)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('message',)
    filter_vertical = ('customers',)
