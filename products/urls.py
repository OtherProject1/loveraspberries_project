from django.contrib import admin
from django.urls import path
from products import views
from .views import *

app_name = 'products'

urlpatterns = [
    path('profile/favourites_products/', favorities_products, name='favorites'),
    path('profile/', profile, name='profile'),
    path('profile/shopping_cart/', shopping_cart, name='shopping_cart'),
    path('profile/delivery/', delivery, name='delivery'),
]
