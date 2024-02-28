from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from products.mixins import BaseMixin
from users.forms import UserLoginForm, UserRegistrationForm
from django.urls import reverse, reverse_lazy
from users.models import User
from django.contrib import auth
from django.contrib.auth.views import PasswordChangeView


class UserLoginView(BaseMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('products:home')


class UserRegistrationView(CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('products:home')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('products:home'))
