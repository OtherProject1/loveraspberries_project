from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('accounts/profile/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('logout/', logout, name='logout'),
]
