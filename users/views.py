from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from products.mixins import BaseMixin
from users.forms import UserLoginForm, UserRegistrationForm
from django.urls import reverse, reverse_lazy
from users.models import User
from django.contrib import auth


class UserLoginView(BaseMixin, LoginView):
    template_name = 'products/base.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('products:home')


class UserRegistrationView(CreateView):
    model = User
    template_name = 'products/base.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('products:home')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('products:home'))
