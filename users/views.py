from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from products.mixins import BaseMixin
from users.forms import UserLoginForm, UserRegistrationForm
from django.urls import reverse, reverse_lazy
from users.models import User


class UserLoginView(BaseMixin, LoginView):
    template_name = 'products/main.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('products:home')


class UserRegistrationView(BaseMixin, CreateView):
    template_name = 'products/main.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('products:home')


