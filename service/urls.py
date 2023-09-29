from django.urls import path
from service.apps import ServiceConfig
from service.views import (HomeTemplateView, CustomerListView, MailingListView, MessageListView, MessageDetailView,
                           MailingCreateView, MessageDeleteView, CustomerCreateView, CustomerDetailView,
                           CustomerUpdateView, CustomerDeleteView, MessageCreateView, MessageUpdateView,
                           MailingDetailView, MailingUpdateView, MailingDeleteView)

app_name = ServiceConfig.name

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),

    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customers/create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer'),
    path('customers/update/<int:pk>/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/delete/<int:pk>/', CustomerDeleteView.as_view(), name='customer_delete'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('services/', MailingListView.as_view(), name='mailings'),
    path('services/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('services/<int:pk>/', MailingDetailView.as_view(), name='mailing'),
    path('services/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('services/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
]
