from django.urls import path
from orders.views import *

app_name = 'orders'

urlpatterns = [
    path('orders/', OrderCreateView.as_view(), name='order'),

]
