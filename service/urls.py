from django.urls import path
from service.apps import ServiceConfig
from service.views import (HomeTemplateView, CustomerListView, ServiceListView, MessageListView, MessageDetailView,
                           ServiceCreateView, MessageDeleteView, CustomerCreateView, CustomerDetailView,
                           CustomerUpdateView, CustomerDeleteView, MessageCreateView, MessageUpdateView,
                           ServiceDetailView, ServiceUpdateView, ServiceDeleteView)

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

    path('services/', ServiceListView.as_view(), name='services'),
    path('services/create/', ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service'),
    path('services/update/<int:pk>/', ServiceUpdateView.as_view(), name='service_update'),
    path('services/delete/<int:pk>/', ServiceDeleteView.as_view(), name='service_delete'),
]
