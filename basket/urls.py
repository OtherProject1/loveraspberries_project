from django.urls import path
from .views import *

app_name = 'basket'

urlpatterns = [
    path('add_product_to_basket/<int:product_id>/', add_product_to_basket, name='add_product_to_basket'),
    path('minus_product_to_basket/<int:product_id>/', minus_product_to_basket, name='minus_product_to_basket'),
    path('basket/', BasketView.as_view(), name='basket'),
]
