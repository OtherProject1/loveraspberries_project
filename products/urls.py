from django.contrib import admin
from django.urls import path
from products import views
from .views import *

app_name = 'products'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('profile/favourites_products/', favorities_products, name='favourites'),
    path('profile/shopping_cart/', shopping_cart, name='shopping_cart'),
    path('profile/delivery/', delivery, name='delivery'),
    path('services/payment-methods', views.payment_methods, name='payment_methods'),
]
