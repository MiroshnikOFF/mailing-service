from django.urls import path
from django.views.decorators.cache import cache_page

from service.apps import ServiceConfig
from service.views import (HomeTemplateView, CustomerListView, MailingListView, MessageListView, MessageDetailView,
                           MailingCreateView, MessageDeleteView, CustomerCreateView, CustomerDetailView,
                           CustomerUpdateView, CustomerDeleteView, MessageCreateView, MessageUpdateView,
                           MailingDetailView, MailingUpdateView, MailingDeleteView, get_report, LogListView,
                           mailing_toggle_activity)

app_name = ServiceConfig.name

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),

    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customers/create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<slug:slug>/', CustomerDetailView.as_view(), name='customer'),
    path('customers/<slug:slug>/update/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<slug:slug>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<slug:slug>/', MessageDetailView.as_view(), name='message'),
    path('messages/<slug:slug>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<slug:slug>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('services/', MailingListView.as_view(), name='mailings'),
    path('services/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('services/<slug:slug>/', MailingDetailView.as_view(), name='mailing'),
    path('services/<slug:slug>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('services/<slug:slug>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),

    path('report/', get_report, name='report'),
    path('services/<slug:slug>/logs/', LogListView.as_view(), name='logs'),
    path('services/<slug:slug>/activity/', mailing_toggle_activity, name='mailing_activity'),
]
