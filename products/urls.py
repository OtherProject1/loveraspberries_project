from django.contrib import admin
from django.urls import path
from products import views
from .views import *

app_name = 'products'

urlpatterns = [
    path('profile/favourites_products/', favorities_products, name='favorites'),
]