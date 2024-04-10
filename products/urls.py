from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('catalog/<slug:subcategory_slug>/', CatalogListView.as_view(), name='catalog'),
    path('catalog/<slug:subcategory_slug>/<int:product_id>/', ProductDetail.as_view(), name='product_page'),
    path('profile/delivery/', delivery, name='delivery'),
    path('profile/history/', history, name='history'),
    # path('profile/reviews/', reviews, name='reviews'),
    path('services/payment-methods', payment_methods, name='payment_methods'),
    path('services/item-return', item_return, name='item_return'),
    path('services/sale-rules', sale_rules, name='sale_rules'),
    path('services/delivery-rules', delivery_rules, name='delivery_rules'),
    path('services/terms', terms_rules, name='terms_rules'),
    path('services/money-return', money_return, name='money_return'),
    path('services/policy-rules', policy, name='policy'),
    path('services/sale-on-market', sale_on_market, name='sale_on_market'),
    path('services/point-promo', point_promo, name='point_promo'),
    path('services/guru', guru, name='guru'),
    path('services/all_work', all_work, name='all_work'),
    path('services/digital', digital, name='digital'),
    path('services/contacts', contacts, name='contacts'),
    path('services/vacancies', vacancies, name='vacancies'),
    path('services/about', about_us, name='about_us'),
    path('services/franchisee/', franchisee, name='franchisee'),
]
