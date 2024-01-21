from django.contrib import admin
from django.urls import path
from products import views
from .views import *

app_name = 'products'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('profile/favourites_products/', favourites_products, name='favourites'),
    path('profile/shopping_cart/', shopping_cart, name='shopping_cart'),
    path('profile/delivery/', delivery, name='delivery'),
    path('services/payment-methods', views.payment_methods, name='payment_methods'),
    path('services/item-return', views.item_return, name='item_return'),
    path('services/sale-rules', views.sale_rules, name='sale_rules'),
    path('services/delivery-rules', views.delivery_rules, name='delivery_rules'),
    path('services/terms', views.terms_rules, name='terms_rules'),
    path('services/money-return', views.money_return, name='money_return'),
    path('services/policy-rules', views.policy, name='policy'),
    path('services/sale-on-market', views.sale_on_market, name='sale_on_market'),
    path('services/franchisee/', views.franchisee, name='franchisee'),
]
