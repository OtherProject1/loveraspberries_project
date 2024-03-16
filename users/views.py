from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from products.mixins import BaseMixin
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import ListView, DetailView

from users.forms import UserLoginForm, UserRegistrationForm
from users.models import User
from basket.models import Favorites


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


class ProfileView(BaseMixin, DetailView):
    model = User
    template_name = 'users/profile.html'

    def get_object(self, queryset=None) -> Model:
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites_products'] = Favorites.objects.filter(user=self.request.user)
        return context