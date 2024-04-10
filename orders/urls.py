from django.urls import path
from orders.views import *

app_name = 'orders'

urlpatterns = [
    path('orders/', OrderCreateView.as_view(), name='order'),
    path('orders-canceled/', CancelView.as_view(), name='order-canceled'),
    path('orders/stripe-webhook', my_webhook_view, name='stripe-webhook'),

]
